from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone

IMMERSION_CATEGORY_CHOICES = [
    ('active', 'Active immersion'),
    ('passive', 'Passive immersion'),
]


class Journal(models.Model):
    hours = models.PositiveIntegerField()
    minutes = models.PositiveIntegerField()
    category = models.CharField(choices=IMMERSION_CATEGORY_CHOICES, max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    time = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.category} {self.hours:02d}:{self.minutes:02d}'

    def clean(self):
        super().clean()
        if self.hours == 0 and self.minutes == 0:
            raise ValidationError('Immersion can not be shorter than 1 minute')

    def save(self, *args, **kwargs):
        self.hours += self.minutes // 60
        self.minutes %= 60
        super().save(*args, **kwargs)

    @staticmethod
    def sum_up_times(category, username=None):
        ret = {}
        if username is None:
            hours = Journal.objects.filter(category=category)
            minutes = Journal.objects.filter(category=category)
        else:
            user = User.objects.get(username=username)
            hours = Journal.objects.filter(category=category, user=user)
            minutes = Journal.objects.filter(category=category, user=user)

        if hours and minutes:
            hours = hours.aggregate(Sum('hours'))['hours__sum']
            minutes = minutes.aggregate(Sum('minutes'))['minutes__sum']

            hours += minutes // 60
            minutes %= 60
        else:
            hours = 0
            minutes = 0

        ret['hours'] = '%02d' % hours
        ret['minutes'] = '%02d' % minutes

        return ret
