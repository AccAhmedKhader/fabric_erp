"""
Batch model for tracking items by batch.
"""

import uuid
from django.db import models


class Batch(models.Model):
    """
    Batch tracking for inventory items.
    """
    class Meta:
        db_table = 'inventory_batches'
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
        ordering = ['-created_at']

    class BatchStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PARTIALLY_USED = 'partial', 'Partially Used'
        COMPLETED = 'completed', 'Completed'
        EXPIRED = 'expired', 'Expired'
        CANCELLED = 'cancelled', 'Cancelled'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the batch'
    )

    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.CASCADE,
        related_name='batches',
        help_text='The item this batch belongs to'
    )

    batch_number = models.CharField(
        max_length=50,
        help_text='Batch number'
    )

    supplier_batch = models.CharField(
        max_length=50,
        blank=True,
        help_text='Supplier batch reference'
    )

    production_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of production'
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text='Expiry date'
    )

    received_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date received'
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Total quantity in this batch'
    )

    remaining_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Remaining quantity'
    )

    status = models.CharField(
        max_length=20,
        choices=BatchStatus.choices,
        default=BatchStatus.ACTIVE,
        help_text='Batch status'
    )

    notes = models.TextField(
        blank=True,
        help_text='Additional notes'
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
        related_name='created_batches',
        help_text='User who created this batch'
    )

    def __str__(self):
        return f"Batch {self.batch_number} - {self.item.name}"

    def is_expired(self):
        """Check if batch is expired."""
        import datetime
        if self.expiry_date and datetime.date.today() > self.expiry_date:
            return True
        return False

    def update_remaining_quantity(self):
        """Update remaining quantity based on stock movements."""
        # This would be calculated from related stock movements
        pass