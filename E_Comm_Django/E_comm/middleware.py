from django.contrib.auth import logout
from django.utils import timezone
from django.core.cache import cache
import os
import time

# Store the server start time
SERVER_START_TIME = timezone.now().timestamp()

class ServerRestartLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only process for authenticated users
        if request.user.is_authenticated and hasattr(request, 'session'):
            session_key = request.session.session_key
            cache_key = f'user_session:{session_key}'
            
            # Get the session creation timestamp from cache
            session_timestamp = cache.get(cache_key)
            
            # If session exists but was created before server started, log the user out
            if session_timestamp and session_timestamp < SERVER_START_TIME:
                logout(request)
                # Redirect will happen in the view after this middleware completes
            
        response = self.get_response(request)
        return response