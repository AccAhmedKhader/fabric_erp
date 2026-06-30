"""
User profile model for extended user information.
Separates personal information from the core user model.
"""

import uuid
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """
    Extended user profile with personal and professional information.
    """
    class Meta:
        db_table = 'auth_user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    class Language(models.TextChoices):
        ARABIC = 'ar', 'العربية'
        ENGLISH = 'en', 'English'
        FRENCH = 'fr', 'Français'

    class Theme(models.TextChoices):
        LIGHT = 'light', 'Light'
        DARK = 'dark', 'Dark'
        SYSTEM = 'system', 'System Default'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the profile'
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text='User associated with this profile'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Profile picture/avatar'
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Date of birth'
    )

    gender = models.CharField(
        max_length=10,
        blank=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ],
        help_text='Gender'
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
        help_text='Nationality'
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        help_text='Department/Division'
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
        help_text='Job title'
    )

    employee_id = models.CharField(
        max_length=50,
        blank=True,
        help_text='Employee ID'
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_reports',
        help_text='Direct manager/supervisor'
    )

    hire_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of hire'
    )

    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH,
        help_text='Preferred language'
    )

    theme = models.CharField(
        max_length=10,
        choices=Theme.choices,
        default=Theme.SYSTEM,
        help_text='Preferred theme'
    )

    timezone = models.CharField(
        max_length=50,
        default='Africa/Cairo',
        help_text='Preferred timezone'
    )

    email_notifications = models.BooleanField(
        default=True,
        help_text='Receive email notifications'
    )

    push_notifications = models.BooleanField(
        default=True,
        help_text='Receive push notifications'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when profile was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when profile was last updated'
    )

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_full_name(self):
        return self.user.get_full_name()

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None