# yourapp/pipeline.py
from django.shortcuts import redirect
from django.urls import reverse

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        # Check if additional info is already filled
        if not user.phone_number:
            return redirect('fill_additional_info')  # URL name for the additional info form
