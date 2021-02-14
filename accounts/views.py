from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def redirect_user(request):
    return redirect(f'/{request.user.username}/')