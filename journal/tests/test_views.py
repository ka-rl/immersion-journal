import unittest
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.http import HttpRequest

from journal.forms import JournalForm
from journal.views import user_page, delete_last

from django.test import TestCase
from journal.models import Journal


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'journal/home.html')

    def test_home_page_dose_not_contain_item_form(self):
        response = self.client.get('/')
        self.assertNotContains(response, JournalForm().as_p())


class UserPageTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('karolina', 'karolina@example.com', 'password')
        self.client.force_login(self.user)

    def test_for_invalid_input_doesnt_save_but_shows_error(self):
        response = self.client.post(f'/{self.user.username}/',
                                    data={'hours': '00', 'minutes': '00', 'category': 'active'})
        self.assertEqual(Journal.objects.count(), 0)
        self.assertContains(response, 'Immersion can not be shorter than 1 minute')

    def test_request_user_is_saved_with_Journal(self):
        self.client.post(f'/{self.user.username}/',
                         data={'hours': '01', 'minutes': '01', 'category': 'active'})
        self.assertEqual(Journal.objects.first().user, self.user)

    def test_user_url_resolves_to_user_page_view(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertTemplateUsed(response, 'journal/user.html')

    def test_user_page_contains_item_form(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertIsInstance(response.context['form'], JournalForm)

    def test_returns_403_if_user_access_not_their_journal(self):
        request = self.client.get('/test/')
        self.assertEqual(request.status_code, 403)

    def test_redirects_to_login_if_user_not_auth(self):
        self.client.logout()
        request = self.client.get('/test/')
        self.assertRedirects(request, '/accounts/login/?next=/test/')


@patch('journal.views.Journal.sum_up_times')
@patch('journal.views.JournalForm')
class UserPageUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['hours'] = '12'
        self.request.POST['minutes'] = '12'
        self.request.POST['category'] = '12'
        self.request.user = Mock(username='karolina', is_authenticated=True)

    def test_passes_POST_data_to_JournalForm(self, mockJournalForm, mockSumUpTimes):
        user_page(self.request, self.request.user.username)
        mockJournalForm.assert_called_once_with(data=self.request.POST)

    def test_does_not_save_if_form_invalid(self, mockJournalForm, mockSumUpTimes):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = False
        user_page(self.request, self.request.user.username)
        self.assertFalse(mock_form.save.called)

    @patch('journal.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockJournalForm, mockSumUpTimes):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = True

        response = user_page(self.request, self.request.user.username)

        self.assertEqual(response, mock_redirect.return_value)
        self.assertTrue(mock_form.save.called)

    @patch('journal.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mockJournalForm, mockSumUpTimes):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = False
        mockSumUpTimes.return_value = {'hours': '00', 'minutes': '00'}

        response = user_page(self.request, self.request.user.username)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'journal/user.html',
            {'active': {'hours': '00', 'minutes': '00'}, 'passive': {'hours': '00', 'minutes': '00'}, 'form': mock_form}
        )


@patch('journal.views.Journal.delete_last')
class UserPageUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = Mock(username='karolina', is_authenticated=True)

    @patch('journal.views.redirect')
    def test_redirects_user_page_after_calling_delete_last(
            self, mock_redirect, mock_delete_last):
        response = delete_last(self.request, self.request.user.username)

        self.assertEqual(response, mock_redirect.return_value)
        self.assertTrue(mock_delete_last.called)
