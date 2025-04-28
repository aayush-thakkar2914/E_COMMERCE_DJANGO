from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

from ..forms import CustomLoginForm

# Function to create a cache key for the session
def get_session_cache_key(session_key):
    return f'user_session:{session_key}'

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    When a user logs in, store their session key in cache with a timestamp
    This will be checked against server start time
    """
    if not hasattr(request, 'session'):
        return
    
    cache_key = get_session_cache_key(request.session.session_key)
    cache.set(cache_key, timezone.now().timestamp(), timeout=settings.SESSION_COOKIE_AGE)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'E_comm/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)  
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomLoginForm()  
    return render(request, 'E_comm/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')