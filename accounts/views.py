from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


@login_required
def redirect_user(request):
    return redirect(f'/{request.user.username}/')


def register(request):
    form = UserCreationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(f'/{user.username}/')
    return render(request, 'accounts/register.html', {'form': form})
