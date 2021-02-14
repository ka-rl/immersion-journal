from django.urls import path, include
from accounts import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('user', views.redirect_user, name='user_redirect')
]
