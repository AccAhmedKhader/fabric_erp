"""
Many-to-many relationship between users and branches.
Specifies which branches a user has access to.
"""

import uuid
from django.db import models
from django.conf import settings


class UserBranch(models.Model):
    """
    Many-to-many relationship between users and branches.
    """
    class Meta:
        db_table = 'common_user_branches'
        verbose_name = 'User Branch'
        verbose_name_plural = 'User Branches'
        unique_together = [['user', 'branch']]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_branches',
        help_text='User with access to this branch'
    )

    branch = models.ForeignKey(
        'common.Branch',
        on_delete=models.CASCADE,
        related_name='user_branches',
        help_text='Branch that the user has access to'
    )

    is_default = models.BooleanField(
        default=False,
        help_text='Whether this is the user\'s default branch'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when user was assigned to this branch'
    )

    def __str__(self):
        return f"{self.user.username} - {self.branch.name}"