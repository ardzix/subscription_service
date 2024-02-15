from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),
    path('tenants/<int:tenant_id>/', views.edit_tenant, name='edit_tenant'),
    path('tenants/', views.manage_tenants, name='manage_tenants'),
    path('manage_subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
    path('additional-info/', views.fill_additional_info, name='fill_additional_info'),

    # Add other paths as necessary
]
