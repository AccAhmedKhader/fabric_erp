"""
Feature flags for controlling feature availability.
"""

import uuid
from django.db import models
from django.utils import timezone


class FeatureFlag(models.Model):
    """
    Feature flag for enabling/disabling features across the application.
    """
    class Meta:
        db_table = 'common_feature_flags'
        verbose_name = 'Feature Flag'
        verbose_name_plural = 'Feature Flags'
        ordering = ['module', 'name']

    class FeatureStatus(models.TextChoices):
        ENABLED = 'enabled', 'Enabled'
        DISABLED = 'disabled', 'Disabled'
        BETA = 'beta', 'Beta'
        DEPRECATED = 'deprecated', 'Deprecated'
        MAINTENANCE = 'maintenance', 'Under Maintenance'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        help_text='Feature name'
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique feature code'
    )

    module = models.CharField(
        max_length=50,
        help_text='Module that owns this feature'
    )

    description = models.TextField(
        blank=True,
        help_text='Feature description'
    )

    status = models.CharField(
        max_length=20,
        choices=FeatureStatus.choices,
        default=FeatureStatus.ENABLED,
        help_text='Current status of the feature'
    )

    require_staff = models.BooleanField(
        default=False,
        help_text='Only staff users can access'
    )

    require_superuser = models.BooleanField(
        default=False,
        help_text='Only superusers can access'
    )

    require_permissions = models.ManyToManyField(
        'authentication.EnterprisePermission',
        blank=True,
        related_name='feature_flags',
        help_text='Permissions required to access'
    )

    rollout_percentage = models.IntegerField(
        default=100,
        help_text='Percentage of users to enable this feature for (0-100)'
    )

    environments = models.JSONField(
        default=list,
        help_text='List of environments where this feature is enabled'
    )

    valid_from = models.DateTimeField(
        default=timezone.now,
        help_text='When the feature becomes available'
    )

    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the feature expires'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_feature_flags'
    )

    def __str__(self):
        return f"{self.module}.{self.code} - {self.status}"

    def is_enabled_for_user(self, user):
        """
        Check if the feature is enabled for a specific user.
        """
        if self.status == self.FeatureStatus.DISABLED:
            return False
        if self.status == self.FeatureStatus.MAINTENANCE:
            return False

        now = timezone.now()
        if now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False

        if self.require_superuser and not user.is_superuser:
            return False
        if self.require_staff and not user.is_staff:
            return False

        if self.rollout_percentage < 100:
            user_hash = hash(str(user.id)) % 100
            if user_hash >= self.rollout_percentage:
                return False

        from django.conf import settings
        if self.environments and settings.ENVIRONMENT not in self.environments:
            return False

        return True

    @classmethod
    def get_feature_value(cls, code, user, default=False):
        """
        Get the value of a feature flag for a user.
        """
        try:
            flag = cls.objects.get(code=code)
            return flag.is_enabled_for_user(user)
        except cls.DoesNotExist:
            return default