from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from tenant.models import Tanant


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_tenant_with_user(sender, instance, **kwargs):
    if hasattr(instance, 'tenant_user'):
        instance.tenant_user.delete()

# Signal to delete associated User when Broker is deleted
@receiver(post_delete, sender=Tanant)
def delete_user_with_tenant(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
