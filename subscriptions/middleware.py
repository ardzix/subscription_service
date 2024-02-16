from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # Check for the flag in the user model or session
            needs_completion = getattr(request.user, 'profile_needs_completion', False) or request.session.get('profile_needs_completion', False)
            if needs_completion and request.path != reverse('fill_additional_info'):
                return redirect('fill_additional_info')
        return response
