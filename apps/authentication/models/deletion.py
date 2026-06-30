"""
Soft delete mixin for user models.
"""

from django.db import models
from django.utils import timezone


class SoftDeleteMixin(models.Model):
    """
    Mixin that adds soft delete functionality to models.
    """
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(
        default=False,
        help_text='Whether this record has been soft deleted'
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time when record was deleted'
    )

    deleted_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_deletions',
        help_text='User who deleted this record'
    )

    def soft_delete(self, deleted_by=None):
        """
        Soft delete this record.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if deleted_by:
            self.deleted_by = deleted_by
        self.save()

    def restore(self):
        """
        Restore a soft-deleted record.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()