import unittest
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.http import HttpRequest
from accounts import views


class UserRedirectUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = Mock(username='karolina', is_authenticated=True)

    @patch('accounts.views.redirect')
    def test_redirects_to_user_site(self, mock_redirect):
        response = views.redirect_user(self.request)

        self.assertEqual(response, mock_redirect.return_value)
