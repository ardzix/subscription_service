"""
URL configuration for subscription_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from subscriptions.views import home, login_view, profile_redirect, terms_and_conditions, privacy_policy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', include('subscriptions.urls')),  

    path('accounts/profile/', profile_redirect, name='profile_redirect'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/login/', login_view, name='login'),
    path('terms/', terms_and_conditions, name='terms'),
    path('privacy/', privacy_policy, name='privacy'),
    path('', home, name='home'),
]
