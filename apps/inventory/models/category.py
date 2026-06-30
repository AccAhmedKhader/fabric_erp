"""
Category model for inventory items.
"""

import uuid
from django.db import models


class Category(models.Model):
    """
    Category for classifying inventory items.
    """
    class Meta:
        db_table = 'inventory_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['company__name', 'name']

    class CategoryType(models.TextChoices):
        FABRIC = 'fabric', 'Fabric'
        GARMENT = 'garment', 'Garment'
        ACCESSORY = 'accessory', 'Accessory'
        RAW_MATERIAL = 'raw', 'Raw Material'
        FINISHED = 'finished', 'Finished Product'
        OTHER = 'other', 'Other'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the category'
    )

    company = models.ForeignKey(
        'common.Company',
        on_delete=models.CASCADE,
        related_name='categories',
        help_text='Company that owns this category'
    )

    name = models.CharField(
        max_length=255,
        help_text='Category name'
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique category code'
    )

    category_type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        default=CategoryType.OTHER,
        help_text='Type of category'
    )

    description = models.TextField(
        blank=True,
        help_text='Category description'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text='Parent category'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether this category is active'
    )

    is_system = models.BooleanField(
        default=False,
        help_text='Whether this is a system category'
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
        related_name='created_categories',
        help_text='User who created this category'
    )

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Get the full category path."""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name