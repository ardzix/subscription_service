from django.db import models
from datetime import timedelta
from libs.storage import FILE_STORAGE
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Module(models.Model):
    name = models.CharField(max_length=255)
    # Removed the api_call_limit and active_user_limit from here

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.FileField(
        storage=FILE_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    modules = models.ManyToManyField('Module')
    max_user = models.IntegerField()
    api_call_limit = models.IntegerField()
    monthly_price = models.DecimalField(max_digits=19, decimal_places=2)
    annual_price = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_highlighted = models.BooleanField(default=False)
    # Removed the original price field for clarity

    @property
    def discounted_monthly_price(self):
        return (1 - self.discount/100) * self.monthly_price
    
    @property
    def discounted_annual_price(self):
        return (1 - self.discount/100) * self.annual_price

    def __str__(self):
        return self.name

class Benefit(models.Model):
    package = models.ForeignKey(Package, related_name='benefits', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description

class Subscription(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    extra_user = models.IntegerField(default=0)
    extra_api_call_limit = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    # extra_user and extra_api_call_limit allow for flexibility in subscriptions

    def renew_subscription(self, days=30):
        """Renews the subscription for another month."""
        self.end_date += timedelta(days=days)
        self.save()

    @property
    def total_user_limit(self):
        """Calculate total user limit including base package and extra users."""
        return self.package.max_user + self.extra_user

    @property
    def total_api_call_limit(self):
        """Calculate total API call limit including base package and extra."""
        return self.package.api_call_limit + self.extra_api_call_limit

    def __str__(self):
        return f'{self.tenant.__str__()} - {self.package.__str__()}'
