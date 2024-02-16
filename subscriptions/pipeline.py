# yourapp/pipeline.py
from django.shortcuts import redirect
from django.urls import reverse

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' and not user.phone_number:
        # Set a flag in the session
        backend.strategy.session_set('profile_needs_completion', True)
