"""
Stock movement model for tracking inventory transactions.
"""

import uuid
from django.db import models
from django.conf import settings


class StockMovement(models.Model):
    """
    Record of stock movement transactions.
    """
    class Meta:
        db_table = 'inventory_stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']

    class MovementType(models.TextChoices):
        PURCHASE_IN = 'purchase_in', 'Purchase In'
        SALE_OUT = 'sale_out', 'Sale Out'
        TRANSFER_IN = 'transfer_in', 'Transfer In'
        TRANSFER_OUT = 'transfer_out', 'Transfer Out'
        ADJUSTMENT_IN = 'adjustment_in', 'Adjustment In'
        ADJUSTMENT_OUT = 'adjustment_out', 'Adjustment Out'
        RETURN_IN = 'return_in', 'Return In'
        RETURN_OUT = 'return_out', 'Return Out'
        WASTAGE = 'wastage', 'Wastage'
        SAMPLE = 'sample', 'Sample'
        OTHER = 'other', 'Other'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the movement'
    )

    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.CASCADE,
        related_name='stock_movements',
        help_text='The item being moved'
    )

    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.CASCADE,
        related_name='stock_movements',
        help_text='Warehouse location'
    )

    # For variants if applicable
    size_color_variant = models.ForeignKey(
        'inventory.SizeColorMatrix',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        help_text='Variant if applicable'
    )

    # For fabric rolls
    fabric_roll = models.ForeignKey(
        'inventory.FabricRoll',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        help_text='Fabric roll if applicable'
    )

    batch = models.ForeignKey(
        'inventory.Batch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        help_text='Batch if applicable'
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        help_text='Type of movement'
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Quantity moved'
    )

    unit = models.CharField(
        max_length=10,
        help_text='Unit of measure'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Unit price'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Total amount'
    )

    reference_type = models.CharField(
        max_length=50,
        blank=True,
        help_text='Reference document type (e.g., Purchase Order, Sales Order)'
    )

    reference_id = models.UUIDField(
        null=True,
        blank=True,
        help_text='Reference document ID'
    )

    reference_number = models.CharField(
        max_length=50,
        blank=True,
        help_text='Reference document number'
    )

    notes = models.TextField(
        blank=True,
        help_text='Additional notes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_stock_movements',
        help_text='User who created this movement'
    )

    def __str__(self):
        return f"{self.movement_type} - {self.quantity} {self.unit} of {self.item.name}"

    def save(self, *args, **kwargs):
        """Override save to calculate total amount."""
        if self.price and self.quantity:
            self.total_amount = self.price * self.quantity
        super().save(*args, **kwargs)