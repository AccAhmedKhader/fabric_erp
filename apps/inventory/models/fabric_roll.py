"""
Fabric Roll model for textile inventory tracking.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator


class FabricRoll(models.Model):
    """
    Individual fabric roll tracking with detailed attributes.
    """
    class Meta:
        db_table = 'inventory_fabric_rolls'
        verbose_name = 'Fabric Roll'
        verbose_name_plural = 'Fabric Rolls'
        ordering = ['-created_at']

    class QualityStatus(models.TextChoices):
        FIRST = 'first', 'First Quality'
        SECOND = 'second', 'Second Quality'
        THIRD = 'third', 'Third Quality'
        REJECTED = 'rejected', 'Rejected'
        SAMPLE = 'sample', 'Sample'

    class FabricType(models.TextChoices):
        COTTON = 'cotton', 'Cotton'
        POLYESTER = 'polyester', 'Polyester'
        LINEN = 'linen', 'Linen'
        WOOL = 'wool', 'Wool'
        SILK = 'silk', 'Silk'
        DENIM = 'denim', 'Denim'
        JERSEY = 'jersey', 'Jersey'
        OTHER = 'other', 'Other'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the fabric roll'
    )

    item = models.ForeignKey(
        'inventory.Item',
        on_delete=models.CASCADE,
        related_name='fabric_rolls',
        help_text='The item this roll belongs to'
    )

    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.CASCADE,
        related_name='fabric_rolls',
        help_text='Warehouse location'
    )

    # Roll identification
    roll_number = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique roll number'
    )

    batch_number = models.CharField(
        max_length=50,
        blank=True,
        help_text='Batch number for this roll'
    )

    dye_lot_number = models.CharField(
        max_length=50,
        blank=True,
        help_text='Dye lot number'
    )

    supplier_batch = models.CharField(
        max_length=50,
        blank=True,
        help_text='Supplier batch reference'
    )

    # Physical measurements
    length_meters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Length in meters'
    )

    width_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Width in centimeters'
    )

    weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Weight in kilograms'
    )

    weight_per_meter = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Weight per meter in kg'
    )

    # Color and design
    color = models.CharField(
        max_length=100,
        blank=True,
        help_text='Color of the fabric'
    )

    color_code = models.CharField(
        max_length=20,
        blank=True,
        help_text='Color code'
    )

    pattern = models.CharField(
        max_length=100,
        blank=True,
        help_text='Pattern/design name'
    )

    # Quality and defects
    quality_status = models.CharField(
        max_length=20,
        choices=QualityStatus.choices,
        default=QualityStatus.FIRST,
        help_text='Quality status'
    )

    fabric_type = models.CharField(
        max_length=20,
        choices=FabricType.choices,
        default=FabricType.OTHER,
        help_text='Type of fabric'
    )

    defects = models.TextField(
        blank=True,
        help_text='List of defects found'
    )

    # Tracking
    received_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date when roll was received'
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text='Expiry date if applicable'
    )

    # Status
    is_available = models.BooleanField(
        default=True,
        help_text='Whether the roll is available'
    )

    is_reserved = models.BooleanField(
        default=False,
        help_text='Whether the roll is reserved'
    )

    is_damaged = models.BooleanField(
        default=False,
        help_text='Whether the roll is damaged'
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
        related_name='created_fabric_rolls',
        help_text='User who created this roll'
    )

    def __str__(self):
        return f"Roll {self.roll_number} - {self.color} - {self.length_meters}m"

    def save(self, *args, **kwargs):
        """Override save to calculate weight per meter if not provided."""
        if not self.weight_per_meter and self.length_meters > 0:
            self.weight_per_meter = self.weight_kg / self.length_meters
        super().save(*args, **kwargs)

    def is_roll_available(self):
        """Check if the roll is available for use."""
        return self.is_available and not self.is_reserved and not self.is_damaged