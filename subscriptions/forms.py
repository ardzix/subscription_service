from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tenant, Subscription, Package

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Include a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name']
        

class SubscriptionForm(forms.ModelForm):
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]
    package = forms.ModelChoiceField(queryset=Package.objects.all(), required=True)
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.none(), required=True)  # Placeholder, will be updated in __init__
    duration = forms.ChoiceField(choices=DURATION_CHOICES, required=True)

    class Meta:
        model = Subscription
        fields = ('package', 'tenant', 'duration')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['tenant'].queryset = Tenant.objects.filter(owned_by=user)  # Update the queryset based on the user
