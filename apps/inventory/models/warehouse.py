"""
Warehouse model for inventory management.
"""

import uuid
from django.db import models
from django.core.validators import RegexValidator


class Warehouse(models.Model):
    """
    Warehouse/Store location for inventory.
    """
    class Meta:
        db_table = 'inventory_warehouses'
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['company__name', 'name']

    class WarehouseType(models.TextChoices):
        MAIN = 'main', 'Main Warehouse'
        BRANCH = 'branch', 'Branch Store'
        SHOWROOM = 'showroom', 'Showroom'
        FACTORY = 'factory', 'Factory Storage'
        VENDOR = 'vendor', 'Vendor Storage'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the warehouse'
    )

    company = models.ForeignKey(
        'common.Company',
        on_delete=models.CASCADE,
        related_name='warehouses',
        help_text='Company that owns this warehouse'
    )

    branch = models.ForeignKey(
        'common.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='warehouses',
        help_text='Branch this warehouse belongs to'
    )

    name = models.CharField(
        max_length=255,
        help_text='Warehouse name'
    )

    code = models.CharField(
        max_length=20,
        help_text='Unique warehouse code'
    )

    warehouse_type = models.CharField(
        max_length=20,
        choices=WarehouseType.choices,
        default=WarehouseType.MAIN,
        help_text='Type of warehouse'
    )

    address = models.TextField(
        blank=True,
        help_text='Warehouse address'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message='Phone number must be valid'
            )
        ]
    )

    manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_warehouses',
        help_text='Warehouse manager'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether this warehouse is active'
    )

    is_default = models.BooleanField(
        default=False,
        help_text='Whether this is the default warehouse'
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
        related_name='created_warehouses',
        help_text='User who created this warehouse'
    )

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    def save(self, *args, **kwargs):
        """Override save to ensure unique code per company."""
        if not self.code:
            # Generate code from name if not provided
            self.code = self.name[:10].upper().replace(' ', '_')
        super().save(*args, **kwargs)