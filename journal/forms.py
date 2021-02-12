from django import forms

from journal.models import Journal


class JournalForm(forms.models.ModelForm):
    class Meta:
        model = Journal
        fields = ('hours', 'minutes', 'category',)

        widgets = {
            'hours': forms.NumberInput(attrs={
                'placeholder': 'HH',
            }),
            'minutes': forms.NumberInput(attrs={
                'placeholder': 'MM',
            }),
        }
