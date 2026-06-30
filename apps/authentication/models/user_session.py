"""
User session model for tracking active user sessions.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class UserSession(models.Model):
    """
    Model for tracking active user sessions.
    """
    class Meta:
        db_table = 'auth_user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the session'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_sessions',
        help_text='User associated with this session'
    )

    session_key = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
        help_text='Django session key'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when session was created'
    )

    expires_at = models.DateTimeField(
        help_text='Date and time when session expires'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address from which session was created'
    )

    user_agent = models.TextField(
        blank=True,
        help_text='User agent from which session was created'
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

    is_active = models.BooleanField(
        default=True,
        help_text='Whether this session is still active'
    )

    last_activity = models.DateTimeField(
        auto_now=True,
        help_text='Date and time of last activity in this session'
    )

    def __str__(self):
        return f"Session {self.session_key} for {self.user.username}"

    def is_expired(self):
        """Check if the session has expired."""
        return timezone.now() > self.expires_at

    def extend_session(self, duration_seconds=None):
        """
        Extend the session expiration time.
        """
        if duration_seconds is None:
            duration_seconds = settings.SESSION_COOKIE_AGE
        self.expires_at = timezone.now() + timezone.timedelta(seconds=duration_seconds)
        self.save(update_fields=['expires_at'])

    def terminate(self):
        """
        Terminate the session.
        """
        self.is_active = False
        self.save(update_fields=['is_active'])