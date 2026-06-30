"""
Many-to-many relationship between users and companies.
Specifies which companies a user has access to.
"""

import uuid
from django.db import models
from django.conf import settings


class UserCompany(models.Model):
    """
    Many-to-many relationship between users and companies.
    """
    class Meta:
        db_table = 'common_user_companies'
        verbose_name = 'User Company'
        verbose_name_plural = 'User Companies'
        unique_together = [['user', 'company']]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_companies',
        help_text='User with access to this company'
    )

    company = models.ForeignKey(
        'common.Company',
        on_delete=models.CASCADE,
        related_name='user_companies',
        help_text='Company that the user has access to'
    )

    is_default = models.BooleanField(
        default=False,
        help_text='Whether this is the user\'s default company'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when user was assigned to this company'
    )

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"