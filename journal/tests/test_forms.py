import unittest
from unittest.mock import patch, Mock
from django.http import HttpRequest

from journal.views import home_page

from django.test import TestCase
from journal.forms import JournalForm


class JournalFormTest(TestCase):
    def test_form_item_input_has_placeholder(self):
        form = JournalForm()
        self.assertIn('placeholder="HH"', form.as_p())
        self.assertIn('placeholder="MM"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = JournalForm(data={'hours': 12, 'category': 'active'})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_00_00_items(self):
        form = JournalForm(data={'hours': 00, 'minutes': 00, 'category': 'active'})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_not_selected_category(self):
        form = JournalForm(data={'hours': 12, 'minutes': 10})
        self.assertFalse(form.is_valid())
