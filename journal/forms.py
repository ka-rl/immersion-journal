from django import forms

from journal.models import Journal

EMPTY_ITEM_ERROR = "Field can't be empty"

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
