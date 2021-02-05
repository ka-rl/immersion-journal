from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

IMMERSION_CATEGORY_CHOICES = [
    ('active', 'Active immersion'),
    ('passive', 'Passive immersion'),
]


# Create your models here.
class Journal(models.Model):
    hours = models.PositiveIntegerField()
    minutes = models.PositiveIntegerField()
    category = models.CharField(choices=IMMERSION_CATEGORY_CHOICES, max_length=7)

    def __str__(self):
        return f'{self.category} {self.hours:02d}:{self.minutes:02d}'

    def clean(self):
        if self.hours == 0 and self.minutes == 0:
            raise ValidationError('Immersion can not be shorter than 1 minutes')
        if self.hours == '' or self.minutes == '':
            raise ValidationError('Fields can not be empty')

        self.hours += self.minutes // 60
        self.minutes %= 60

    @staticmethod
    def sum_up_times(category):
        ret = {'hours': '00', 'minutes': '00'}
        if Journal.objects.filter(category=category).count() > 0:
            hours = Journal.objects.filter(category=category).aggregate(Sum('hours'))['hours__sum']
            minutes = Journal.objects.filter(category=category).aggregate(Sum('minutes'))['minutes__sum']

            hours += minutes // 60
            minutes %= 60

            ret['hours'] = '%02d' % hours
            ret['minutes'] = '%02d' % minutes

        return ret
