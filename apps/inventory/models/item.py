"""
Item model for inventory management.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    """
    Inventory item/product.
    """
    class Meta:
        db_table = 'inventory_items'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['company__name', 'code']

    class ItemType(models.TextChoices):
        FABRIC = 'fabric', 'Fabric'
        GARMENT = 'garment', 'Garment'
        ACCESSORY = 'accessory', 'Accessory'
        RAW_MATERIAL = 'raw', 'Raw Material'
        FINISHED = 'finished', 'Finished Product'
        SERVICE = 'service', 'Service'
        OTHER = 'other', 'Other'

    class UnitOfMeasure(models.TextChoices):
        METER = 'm', 'Meter'
        YARD = 'yd', 'Yard'
        KILOGRAM = 'kg', 'Kilogram'
        GRAM = 'g', 'Gram'
        PIECE = 'pc', 'Piece'
        DOZEN = 'dz', 'Dozen'
        BOX = 'bx', 'Box'
        ROLL = 'rl', 'Roll'
        OTHER = 'other', 'Other'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the item'
    )

    company = models.ForeignKey(
        'common.Company',
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Company that owns this item'
    )

    category = models.ForeignKey(
        'inventory.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items',
        help_text='Item category'
    )

    code = models.CharField(
        max_length=50,
        help_text='Item code/SKU'
    )

    name = models.CharField(
        max_length=255,
        help_text='Item name'
    )

    description = models.TextField(
        blank=True,
        help_text='Item description'
    )

    item_type = models.CharField(
        max_length=20,
        choices=ItemType.choices,
        default=ItemType.OTHER,
        help_text='Type of item'
    )

    primary_unit = models.CharField(
        max_length=10,
        choices=UnitOfMeasure.choices,
        default=UnitOfMeasure.PIECE,
        help_text='Primary unit of measure'
    )

    secondary_unit = models.CharField(
        max_length=10,
        choices=UnitOfMeasure.choices,
        blank=True,
        help_text='Secondary unit of measure'
    )

    conversion_factor = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=1.0,
        help_text='Conversion factor from primary to secondary unit'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether this item is active'
    )

    is_variant = models.BooleanField(
        default=False,
        help_text='Whether this is a variant of another item'
    )

    parent_item = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='variants',
        help_text='Parent item for variants'
    )

    # Stock thresholds
    min_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Minimum stock level'
    )

    max_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Maximum stock level'
    )

    reorder_point = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Reorder point'
    )

    reorder_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Quantity to reorder'
    )

    # Supplier information
    preferred_supplier = models.ForeignKey(
        'purchasing.Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_items',
        help_text='Preferred supplier for this item'
    )

    lead_time_days = models.IntegerField(
        default=0,
        help_text='Lead time in days'
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
        related_name='created_items',
        help_text='User who created this item'
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """Override save to ensure unique code per company."""
        if not self.code:
            self.code = self.name[:20].upper().replace(' ', '_')
        super().save(*args, **kwargs)