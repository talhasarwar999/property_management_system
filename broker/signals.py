from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from broker.models import Broker


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_broker_with_user(sender, instance, **kwargs):
    if hasattr(instance, 'broker_user'):
        instance.broker_user.delete()

@receiver(post_delete, sender=Broker)
def delete_user_with_broker(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
