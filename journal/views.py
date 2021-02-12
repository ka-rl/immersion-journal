from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from journal.forms import JournalForm
from journal.models import Journal


def home_page(request):
    context = {'active': Journal.sum_up_times('active'), 'passive': Journal.sum_up_times('passive')}
    return render(request, 'journal/home.html', context)


@login_required(login_url='/accounts/login/')
def user_page(request, username):
    if request.user.username == username:
        form = JournalForm(data=request.POST)
        context = {'active': Journal.sum_up_times('active', username),
                   'passive': Journal.sum_up_times('passive', username), 'form': form}
        if form.is_valid():
            journal = form.save(commit=False)
            journal.user = request.user
            journal.save()
            return redirect(f'/{username}/', context)
        return render(request, 'journal/user.html', context)
    else:
        return HttpResponseForbidden()
