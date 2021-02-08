import unittest
from unittest.mock import patch, Mock
from django.http import HttpRequest

from journal.forms import JournalForm
from journal.views import home_page

from django.test import TestCase
from journal.models import Journal

from django.core.exceptions import ValidationError


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'journal/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], JournalForm)

    def test_for_invalid_input_doesnt_save_but_shows_error(self):
        response = self.client.post('/', data={'hours': '00', 'minutes': '00', 'category': 'active'})
        self.assertEqual(Journal.objects.count(), 0)
        self.assertContains(response, 'Immersion can not be shorter than 1 minute')


@patch('journal.views.JournalForm')
class HomePageUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['hours'] = '12'
        self.request.POST['minutes'] = '12'
        self.request.POST['category'] = '12'
        self.request.user = Mock()

    def test_passes_POST_data_to_JournalForm(self, mockJournalForm):
        home_page(self.request)
        mockJournalForm.assert_called_once_with(data=self.request.POST)

    def test_does_not_save_if_form_invalid(self, mockJournalForm):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = False
        home_page(self.request)
        self.assertFalse(mock_form.save.called)

    @patch('journal.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockJournalForm
    ):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = True

        response = home_page(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        self.assertTrue(mock_form.save.called)

    @patch('journal.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mockJournalForm
    ):
        mock_form = mockJournalForm.return_value
        mock_form.is_valid.return_value = False

        response = home_page(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'journal/home.html',
            {'active': {'hours': '00', 'minutes': '00'}, 'passive': {'hours': '00', 'minutes': '00'}, 'form': mock_form}
        )
