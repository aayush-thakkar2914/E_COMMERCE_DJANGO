from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from ..forms import CustomUserCreationForm, CustomLoginForm
from ..models import UserProfile

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Send welcome email
            send_welcome_email(user)
            
            # Log the user in
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'E_comm/signup.html', {'form': form})

def send_welcome_email(user):
    """Send a welcome email to the newly registered user"""
    subject = 'Welcome to Our E-Commerce Store!'
    html_message = render_to_string('E_comm/email/welcome_email.html', {
        'username': user.username
    })
    plain_message = strip_tags(html_message)
    
    if user.email:  # Only send if user provided an email
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

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