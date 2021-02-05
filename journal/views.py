from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from journal.models import Journal


def home_page(request):
    stats = {'active': Journal.sum_up_times('active'), 'passive': Journal.sum_up_times('passive')}
    if request.method == 'POST':
        new_item = Journal(hours=request.POST['hours'], minutes=request.POST['minutes'],
                           category=request.POST['category'])
        try:
            new_item.full_clean()
            new_item.save()
            return redirect('/')
        except ValidationError:
            return render(request, 'journal/home.html', stats)
    return render(request, 'journal/home.html', stats)
