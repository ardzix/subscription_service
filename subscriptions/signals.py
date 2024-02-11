from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Subscription
from .utils import send_kafka_message


@receiver(pre_save, sender=Subscription)
def get_prev(sender, instance, **kwargs):
    prev_instance = Subscription.objects.filter(pk=instance.pk).first()
    instance.prev = prev_instance


@receiver(post_save, sender=Subscription)
def subscription_updated(sender, instance, **kwargs):
    # Only proceed if 'is_active' has just been updated to True
    if instance.active:
        # Fetch the previous state of the instance before it was saved
        prev_instance = instance.prev
        # Check if the subscription was just activated (i.e., active was False before save)
        if prev_instance and not prev_instance.active:
            # Calculate the days since the subscription started
            days_since_start = (timezone.now().date() - instance.start_date).days
            
            # Adjust the end_date based on the activation date
            new_end_date = instance.end_date + timezone.timedelta(days=days_since_start)
            Subscription.objects.filter(pk=instance.pk).update(end_date=new_end_date)
            
            # Prepare the message content
            message_content = {
                'subscription_id': instance.id,
                'tenant_id': instance.tenant.id,
                'tenant_name': instance.tenant.name,
                'tenant_phone': instance.tenant.phone_number,
                'tenant_email': instance.tenant.owned_by.email,
                'package_id': instance.package.id,
                'max_user': instance.package.max_user,
                'extra_user': instance.extra_user,
                'max_api_call_limit': instance.package.api_call_limit,
                'extra_api_call_limit': instance.extra_api_call_limit,
                'action': 'activated'  # Assuming you want a specific action for activation
            }
            send_kafka_message('subscription-topic', message_content)
