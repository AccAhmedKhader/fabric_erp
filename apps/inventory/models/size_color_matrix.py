"""
Size and Color Matrix model for garment and fabric variants.
"""

import uuid
from django.db import models


class SizeColorMatrix(models.Model):
    """
    Matrix for managing product variants by size and color.
    """
    class Meta:
        db_table = 'inventory_size_color_matrix'
        verbose_name = 'Size/Color Matrix'
        verbose_name_plural = 'Size/Color Matrices'
        ordering = ['item__name', 'size', 'color']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the matrix entry'
    )

    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.CASCADE,
        related_name='size_color_variants',
        help_text='The item this variant belongs to'
    )

    size = models.CharField(
        max_length=50,
        help_text='Size (e.g., S, M, L, XL, 40, 42, etc.)'
    )

    color = models.CharField(
        max_length=100,
        help_text='Color name'
    )

    color_code = models.CharField(
        max_length=20,
        blank=True,
        help_text='Color code/hex'
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique SKU for this variant'
    )

    barcode = models.CharField(
        max_length=50,
        blank=True,
        help_text='Barcode for this variant'
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Current quantity in stock'
    )

    reserved_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Quantity reserved for orders'
    )

    available_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Quantity available for sale'
    )

    min_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Minimum stock level for this variant'
    )

    max_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Maximum stock level for this variant'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether this variant is active'
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
        related_name='created_size_color_variants',
        help_text='User who created this variant'
    )

    def __str__(self):
        return f"{self.item.name} - {self.size} - {self.color}"

    def calculate_available_quantity(self):
        """Calculate available quantity."""
        self.available_quantity = self.quantity - self.reserved_quantity
        self.save(update_fields=['available_quantity'])
        return self.available_quantity