from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'company_name', 'company_industry', 'is_staff']
    
    # Optionally, customize the form fields shown in the add/change forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'company_name', 'company_industry')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'company_name', 'company_industry')}),
    )

# Unregister the default User admin if it's registered
# This step is only necessary if the default User model is being used elsewhere in admin
# from django.contrib.auth.models import User
# admin.site.unregister(User)

# Register your CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
