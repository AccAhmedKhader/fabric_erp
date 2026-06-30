"""
Branch model for multi-branch support.
Each branch belongs to a company and can have its own settings.
"""

import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Branch(models.Model):
    """
    Branch model for multi-branch support.
    """
    class Meta:
        db_table = 'common_branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['company__name', 'name']
        unique_together = [['company', 'code']]

    class BranchType(models.TextChoices):
        HEADQUARTERS = 'hq', 'Headquarters'
        STORE = 'store', 'Store'
        WAREHOUSE = 'warehouse', 'Warehouse'
        OFFICE = 'office', 'Office'
        SHOWROOM = 'showroom', 'Showroom'
        FACTORY = 'factory', 'Factory'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the branch'
    )

    company = models.ForeignKey(
        'common.Company',
        on_delete=models.CASCADE,
        related_name='branches',
        help_text='Company that this branch belongs to'
    )

    name = models.CharField(
        max_length=255,
        help_text='Branch name'
    )

    code = models.CharField(
        max_length=20,
        help_text='Branch code (unique within company)'
    )

    branch_type = models.CharField(
        max_length=20,
        choices=BranchType.choices,
        default=BranchType.STORE
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

    email = models.EmailField(
        blank=True,
        help_text='Branch email address'
    )

    address = models.TextField(
        blank=True,
        help_text='Branch address'
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default='Egypt'
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_headquarters = models.BooleanField(
        default=False,
        help_text='Whether this is the headquarters'
    )

    opening_time = models.TimeField(
        null=True,
        blank=True,
        help_text='Regular opening time'
    )

    closing_time = models.TimeField(
        null=True,
        blank=True,
        help_text='Regular closing time'
    )

    timezone = models.CharField(
        max_length=50,
        default='Africa/Cairo'
    )

    parent_branch = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_branches',
        help_text='Parent branch if this is a sub-branch'
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
        related_name='created_branches'
    )

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    def get_full_address(self):
        """Get the full formatted address."""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.country:
            parts.append(self.country)
        return ', '.join(parts)

    def soft_delete(self, deleted_by=None):
        """Soft delete the branch."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if deleted_by:
            self.deleted_by = deleted_by
        self.save()