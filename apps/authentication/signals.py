"""
Signal handlers for authentication app.
"""

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, Role, EnterprisePermission
# التعديل المقترح في apps/authentication/signals.py (السطر 9)
from apps.authentication.events import UserCreated, UserUpdated, UserDeactivated, EventDispatcher

User = get_user_model()


@receiver(post_save, sender=User)
def handle_user_created(sender, instance, created, **kwargs):
    """
    Handle user creation events.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
        EventDispatcher().dispatch(UserCreated(instance))


@receiver(post_save, sender=User)
def handle_user_updated(sender, instance, created, **kwargs):
    """
    Handle user update events.
    """
    if not created and not instance.is_active:
        EventDispatcher().dispatch(UserDeactivated(instance))


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    """
    Create default system data after migrations.
    """
    if sender.name == 'apps.authentication':
        Role.create_system_roles()
        EnterprisePermission.create_system_permissions()