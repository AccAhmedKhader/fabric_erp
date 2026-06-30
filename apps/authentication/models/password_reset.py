"""
Password reset token model for secure password reset functionality.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets
import hashlib


class PasswordResetToken(models.Model):
    """
    Model for storing password reset tokens.
    """
    class Meta:
        db_table = 'auth_password_reset'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the token'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        help_text='User requesting password reset'
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text='Hashed token for password reset'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when token was created'
    )

    expires_at = models.DateTimeField(
        help_text='Date and time when token expires'
    )

    is_used = models.BooleanField(
        default=False,
        help_text='Whether this token has been used'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address from which reset was requested'
    )

    user_agent = models.TextField(
        blank=True,
        help_text='User agent from which reset was requested'
    )

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_at}"

    @classmethod
    def generate_token(cls, user):
        """
        Generate a new password reset token for a user.
        """
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

        cls.objects.filter(user=user, is_used=False).delete()

        token = cls.objects.create(
            user=user,
            token=hashed_token,
            expires_at=timezone.now() + timezone.timedelta(hours=24)
        )

        return token, raw_token

    def is_valid(self):
        """
        Check if the token is still valid (not expired and not used).
        """
        return (not self.is_used and
                timezone.now() < self.expires_at)

    def mark_as_used(self):
        """
        Mark the token as used.
        """
        self.is_used = True
        self.save(update_fields=['is_used'])