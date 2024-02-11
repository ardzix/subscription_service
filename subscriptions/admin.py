from django.contrib import admin
from .models import Tenant, Module, Package, Benefit, Subscription

admin.site.register(Tenant)
admin.site.register(Module)
class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1  # How many rows to show

class PackageAdmin(admin.ModelAdmin):
    inlines = [BenefitInline,]

admin.site.register(Package, PackageAdmin)
admin.site.register(Subscription)
