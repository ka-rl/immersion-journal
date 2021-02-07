from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from journal.forms import JournalForm
from journal.models import Journal


def home_page(request):
    form = JournalForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {'active': Journal.sum_up_times('active'), 'passive': Journal.sum_up_times('passive'),
               'form': form}
    return render(request, 'journal/home.html', context)
