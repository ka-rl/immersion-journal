from django.contrib.auth.models import User
from django.test import TestCase
from journal.models import Journal

from django.core.exceptions import ValidationError


class JournalModelTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_cannot_save_empty_fields(self):
        item = Journal(hours=12, minutes=12, category=None, user=self.user)
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_category_have_only_2_options(self):
        self.assertEqual(Journal._meta.get_field('category').choices,
                         [('active', 'Active immersion'), ('passive', 'Passive immersion')])

    def test_string_representation(self):
        item = Journal(hours=1, minutes=0, category='active', user=self.user)
        self.assertEqual(str(item), 'active 01:00')

    def test_cannot_save_immersion_shorter_than_1_minute(self):
        item = Journal(hours=0, minutes=0, category='passive', user=self.user)
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_minutes_over_60_are_covert_to_hours(self):
        item = Journal(hours=0, minutes=80, category='passive', user=self.user)
        item.save()
        self.assertEqual(item.hours, 1)
        self.assertEqual(item.minutes, 20)

    def test_empty_string_raises_validation_error(self):
        item = Journal(hours='01', minutes='', category='passive', user=self.user)
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_string_that_cann_not_be_cover_to_int_raises_validation_error(self):
        item = Journal(hours='acx', minutes='01', category='passive', user=self.user)
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_sum_all_active_times_and_pass_them_as_string(self):
        Journal.objects.create(hours=1, minutes=1, category='active', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='active', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='passive', user=self.user)
        self.assertEqual(Journal.sum_up_times('active'), {'hours': '02', 'minutes': '02'})

    def test_sum_all_passive_times_and_pass_them_as_string(self):
        Journal.objects.create(hours=1, minutes=1, category='passive', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='passive', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='active', user=self.user)
        self.assertEqual(Journal.sum_up_times('passive'), {'hours': '02', 'minutes': '02'})

    def test_sum_up_times_return_00_00_when_objects_do_not_exist(self):
        self.assertEqual(Journal.sum_up_times('passive'), {'hours': '00', 'minutes': '00'})

    def test_sum_up_times_cover_minutes_over_60_to_hours(self):
        Journal.objects.create(hours=1, minutes=50, category='passive', user=self.user)
        Journal.objects.create(hours=1, minutes=20, category='passive', user=self.user)
        self.assertEqual(Journal.sum_up_times('passive'), {'hours': '03', 'minutes': '10'})

    def test_sum_up_times_for_specific_user(self):
        user_two = User.objects.create_user('test2', 'test2@example.com', 'test2')
        Journal.objects.create(hours=1, minutes=1, category='passive', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='passive', user=self.user)
        Journal.objects.create(hours=1, minutes=1, category='passive', user=user_two)
        self.assertEqual(Journal.sum_up_times('passive', self.user.username), {'hours': '02', 'minutes': '02'})

    def test_user_field_is_required(self):
        item = Journal(hours='12', minutes='01', category='passive')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()
