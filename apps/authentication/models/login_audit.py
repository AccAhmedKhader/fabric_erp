"""
Login audit model for tracking authentication attempts.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class LoginAudit(models.Model):
    """
    Audit model for tracking all login attempts.
    """
    class Meta:
        db_table = 'auth_login_audit'
        verbose_name = 'Login Audit'
        verbose_name_plural = 'Login Audits'
        ordering = ['-login_time']

    class LoginStatus(models.TextChoices):
        SUCCESS = 'success', 'Success'
        FAILURE = 'failure', 'Failure'
        LOCKED = 'locked', 'Account Locked'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the audit record'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='login_audits',
        help_text='User who attempted to login'
    )

    username = models.CharField(
        max_length=150,
        help_text='Username used for login attempt'
    )

    login_time = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time of login attempt'
    )

    logout_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time of logout'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the client'
    )

    user_agent = models.TextField(
        blank=True,
        help_text='User agent string from the client'
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
        help_text='Browser name and version'
    )

    device = models.CharField(
        max_length=100,
        blank=True,
        help_text='Device type (desktop, mobile, tablet)'
    )

    status = models.CharField(
        max_length=10,
        choices=LoginStatus.choices,
        default=LoginStatus.SUCCESS,
        help_text='Status of the login attempt'
    )

    failure_reason = models.CharField(
        max_length=255,
        blank=True,
        help_text='Reason for failure if any'
    )

    session_key = models.CharField(
        max_length=40,
        blank=True,
        help_text='Session key associated with this login'
    )

    def __str__(self):
        return f"{self.username} - {self.login_time} - {self.get_status_display()}"

    def set_logout(self):
        """Record the logout time."""
        self.logout_time = timezone.now()
        self.save(update_fields=['logout_time'])

    @property
    def is_success(self):
        return self.status == self.LoginStatus.SUCCESS

    @property
    def is_failure(self):
        return self.status == self.LoginStatus.FAILURE