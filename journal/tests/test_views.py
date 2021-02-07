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

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'hours': '12', 'minutes': '10', 'category': 'active'})
        self.assertEqual(Journal.objects.count(), 1)
        new_item = Journal.objects.first()
        self.assertEqual(new_item.hours, 12)
        self.assertEqual(new_item.minutes, 10)
        self.assertEqual(new_item.category, 'active')

    def test_for_invalid_input_doesnt_save(self):
        self.client.post('/', data={'hours': '00', 'minutes': '00', 'category': 'active'})
        self.assertEqual(Journal.objects.count(), 0)

    def test_redirects_after_POST_with_valid_data(self):
        response = self.client.post('/', data={'hours': '12', 'minutes': '10', 'category': 'active'})
        self.assertRedirects(response, '/')

    def test_renders_home_page_after_POST_with_invalid_data(self):
        response = self.client.post('/', data={'hours': '', 'minutes': '', 'category': 'active'})
        self.assertTrue(response.status_code, 200)

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], JournalForm)
