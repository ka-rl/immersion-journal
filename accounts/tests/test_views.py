import unittest
from unittest.mock import patch, Mock

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from accounts import views
from accounts.views import register


class UserRedirectUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = Mock(username='karolina', is_authenticated=True)

    @patch('accounts.views.redirect')
    def test_redirects_to_user_site(self, mock_redirect):
        response = views.redirect_user(self.request)

        self.assertEqual(response, mock_redirect.return_value)


class RegisterUserTest(TestCase):
    def test_url_resolves_to_register_view(self):
        response = self.client.get(f'/accounts/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_contains_user_form(self):
        response = self.client.get(f'/accounts/register/')
        self.assertIsInstance(response.context['form'], UserCreationForm)


@patch('accounts.views.UserCreationForm')
class RegisterUserUnitTest(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['username'] = 'test'
        self.request.POST['password'] = 'test'

    @patch('accounts.views.login')
    def test_passes_POST_data_to_UserForm(self, mock_login, mockUserCreationForm):
        register(self.request)
        mockUserCreationForm.assert_called_once_with(data=self.request.POST)

    def test_does_not_save_if_form_invalid(self, mockUserCreationForm):
        mock_form = mockUserCreationForm.return_value
        mock_form.is_valid.return_value = False
        register(self.request)
        self.assertFalse(mock_form.save.called)

    @patch('accounts.views.login')
    @patch('accounts.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mock_login, mockUserCreationForm):
        mock_form = mockUserCreationForm.return_value
        mock_form.is_valid.return_value = True

        response = register(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        self.assertTrue(mock_form.save.called)

    @patch('accounts.views.login')
    @patch('accounts.views.render')
    def test_renders_register_view_with_form_if_form_invalid(
            self, mock_render, mock_login, mockUserCreationForm):
        mock_form = mockUserCreationForm.return_value
        mock_form.is_valid.return_value = False

        response = register(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'accounts/register.html', {'form': mock_form}
        )

    @patch('accounts.views.login')
    def test_view_login_user(self, mock_login, mockUserCreationForm):
        register(self.request)
        mock_login.assert_called_once_with(self.request, mockUserCreationForm().save())
