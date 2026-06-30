"""
Company model for multi-tenant support.
All data in the system is isolated by company.
"""

import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Company(models.Model):
    """
    Company model for multi-tenant support.
    """
    class Meta:
        db_table = 'common_companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']

    class CompanyType(models.TextChoices):
        HEADQUARTERS = 'hq', 'Headquarters'
        SUBSIDIARY = 'sub', 'Subsidiary'
        BRANCH = 'branch', 'Branch'
        SHOWROOM = 'showroom', 'Showroom'
        WAREHOUSE = 'warehouse', 'Warehouse'

    class Industry(models.TextChoices):
        TEXTILE = 'textile', 'Textile Trading'
        GARMENT = 'garment', 'Garment Trading'
        MANUFACTURING = 'manufacturing', 'Manufacturing'
        RETAIL = 'retail', 'Retail'
        WHOLESALE = 'wholesale', 'Wholesale'
        ECOMMERCE = 'ecommerce', 'E-commerce'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the company'
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='Company name'
    )

    legal_name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Legal/registered company name'
    )

    company_type = models.CharField(
        max_length=20,
        choices=CompanyType.choices,
        default=CompanyType.HEADQUARTERS,
        help_text='Type of company/entity'
    )

    industry = models.CharField(
        max_length=20,
        choices=Industry.choices,
        default=Industry.TEXTILE,
        help_text='Primary industry'
    )

    tax_id = models.CharField(
        max_length=50,
        blank=True,
        help_text='Tax identification number'
    )

    commercial_register = models.CharField(
        max_length=50,
        blank=True,
        help_text='Commercial registration number'
    )

    registration_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of registration'
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

    mobile = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message='Mobile number must be valid'
            )
        ]
    )

    email = models.EmailField(
        blank=True,
        help_text='Company email address'
    )

    website = models.URLField(
        blank=True,
        help_text='Company website'
    )

    address = models.TextField(
        blank=True,
        help_text='Full address'
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        help_text='State/Province'
    )

    country = models.CharField(
        max_length=100,
        default='Egypt'
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    currency = models.CharField(
        max_length=3,
        default='EGP',
        help_text='Primary currency (ISO code)'
    )

    fiscal_year_start = models.IntegerField(
        default=7,
        help_text='Starting month of fiscal year (1-12)'
    )

    fiscal_year_end = models.IntegerField(
        default=6,
        help_text='Ending month of fiscal year (1-12)'
    )

    timezone = models.CharField(
        max_length=50,
        default='Africa/Cairo'
    )

    date_format = models.CharField(
        max_length=20,
        default='d/m/Y',
        help_text='Date format (PHP date format)'
    )

    time_format = models.CharField(
        max_length=20,
        default='H:i:s',
        help_text='Time format (PHP time format)'
    )

    is_active = models.BooleanField(
        default=True
    )

    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the company has been verified'
    )

    subscription_status = models.CharField(
        max_length=20,
        default='trial',
        choices=[
            ('trial', 'Trial'),
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
        ]
    )

    subscription_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the subscription expires'
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
        related_name='created_companies'
    )

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

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

    def is_subscription_valid(self):
        """Check if the subscription is valid."""
        if self.subscription_status == 'active' and self.subscription_expires_at:
            return timezone.now() < self.subscription_expires_at
        return self.subscription_status == 'active'

    def soft_delete(self, deleted_by=None):
        """Soft delete the company."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if deleted_by:
            self.deleted_by = deleted_by
        self.save()