"""
Email verification token model for verifying user email addresses.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets
import hashlib


class EmailVerification(models.Model):
    """
    Model for storing email verification tokens.
    """
    class Meta:
        db_table = 'auth_email_verification'
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the verification'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_verifications',
        help_text='User whose email is being verified'
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text='Hashed token for email verification'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when token was created'
    )

    expires_at = models.DateTimeField(
        help_text='Date and time when token expires'
    )

    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the email has been verified'
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address from which verification was requested'
    )

    user_agent = models.TextField(
        blank=True,
        help_text='User agent from which verification was requested'
    )

    def __str__(self):
        return f"Email verification for {self.user.username} at {self.created_at}"

    @classmethod
    def generate_token(cls, user):
        """
        Generate a new email verification token for a user.
        """
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

        cls.objects.filter(user=user).delete()

        token = cls.objects.create(
            user=user,
            token=hashed_token,
            expires_at=timezone.now() + timezone.timedelta(days=3)
        )

        return token, raw_token

    def is_valid(self):
        """
        Check if the token is still valid (not expired and not verified).
        """
        return (not self.is_verified and
                timezone.now() < self.expires_at)

    def verify_email(self):
        """
        Verify the email address and mark as verified.
        """
        self.is_verified = True
        self.user.is_email_verified = True
        self.user.save(update_fields=['is_email_verified'])
        self.save(update_fields=['is_verified'])