"""
User model definition for FabricERP.
Extends Django's AbstractUser to add custom fields.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from .deletion import SoftDeleteMixin


class User(AbstractUser, SoftDeleteMixin):
    """
    Custom User model with UUID primary key and additional fields.
    """
    class Meta:
        db_table = 'auth_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the user'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )

    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='Full name of the user'
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        help_text='Email address of the user'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
            )
        ],
        help_text='Phone number with country code'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active.'
    )

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    is_superuser = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when user was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when user was last updated'
    )

    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time of last login'
    )

    is_email_verified = models.BooleanField(
        default=False,
        help_text='Whether the user\'s email has been verified'
    )

    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time when email was verified'
    )

    email_verification_attempts = models.IntegerField(
        default=0,
        help_text='Number of verification attempts'
    )

    failed_login_attempts = models.IntegerField(
        default=0,
        help_text='Number of consecutive failed login attempts'
    )

    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time until the account is locked'
    )

    last_password_change = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time of last password change'
    )

    is_2fa_enabled = models.BooleanField(
        default=False,
        help_text='Whether two-factor authentication is enabled'
    )

    def __str__(self):
        return f"{self.full_name} ({self.username})"

    def get_full_name(self):
        """Return the full name of the user."""
        return self.full_name or self.username

    def get_short_name(self):
        """Return the short name of the user."""
        return self.full_name.split()[0] if self.full_name else self.username

    def is_account_locked(self):
        """Check if the account is currently locked."""
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False

    def lock_account(self, duration_minutes=15):
        """Lock the account for the specified duration."""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['locked_until'])

    def unlock_account(self):
        """Unlock the account."""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['locked_until', 'failed_login_attempts'])

    def increment_failed_attempts(self):
        """Increment the failed login attempts counter."""
        self.failed_login_attempts += 1
        self.save(update_fields=['failed_login_attempts'])

    def reset_failed_attempts(self):
        """Reset the failed login attempts counter."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])

    def verify_email(self):
        """Mark email as verified."""
        self.is_email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=['is_email_verified', 'email_verified_at'])

    def has_company_access(self, company_id):
        """Check if user has access to a specific company."""
        if self.is_superuser:
            return True
        from apps.common.models import UserCompany
        return UserCompany.objects.filter(user=self, company_id=company_id).exists()

    def has_branch_access(self, branch_id):
        """Check if user has access to a specific branch."""
        if self.is_superuser:
            return True
        from apps.common.models import UserBranch
        return UserBranch.objects.filter(user=self, branch_id=branch_id).exists()

    def save(self, *args, **kwargs):
        """Override save to ensure full_name is set."""
        if not self.full_name:
            self.full_name = self.username
        super().save(*args, **kwargs)