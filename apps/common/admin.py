"""
Admin configuration for common models.
"""

from django.contrib import admin
from .models import Company, Branch, FeatureFlag


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Company admin configuration.
    """
    list_display = ('name', 'tax_id', 'industry', 'country', 'is_active')
    list_filter = ('industry', 'country', 'is_active')
    search_fields = ('name', 'legal_name', 'tax_id')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {'fields': ('name', 'legal_name', 'company_type', 'industry')}),
        ('Registration', {'fields': ('tax_id', 'commercial_register', 'registration_date')}),
        ('Contact', {'fields': ('phone', 'mobile', 'email', 'website')}),
        ('Address', {'fields': ('address', 'city', 'state', 'country', 'postal_code')}),
        ('Financial', {'fields': ('currency', 'fiscal_year_start', 'fiscal_year_end')}),
        ('Settings', {'fields': ('timezone', 'date_format', 'time_format')}),
        ('Status', {'fields': ('is_active', 'is_verified', 'subscription_status', 'subscription_expires_at')}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """
    Branch admin configuration.
    """
    list_display = ('name', 'code', 'company', 'branch_type', 'is_headquarters', 'is_active')
    list_filter = ('company', 'branch_type', 'is_active', 'is_headquarters')
    search_fields = ('name', 'code', 'address')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {'fields': ('company', 'name', 'code', 'branch_type')}),
        ('Contact', {'fields': ('phone', 'email')}),
        ('Address', {'fields': ('address', 'city', 'state', 'country', 'postal_code')}),
        ('Settings', {'fields': ('is_active', 'is_headquarters', 'opening_time', 'closing_time', 'timezone')}),
        ('Hierarchy', {'fields': ('parent_branch',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    """
    Feature flag admin configuration.
    """
    list_display = ('code', 'name', 'module', 'status', 'rollout_percentage')
    list_filter = ('module', 'status', 'created_at')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {'fields': ('code', 'name', 'module', 'description')}),
        ('Status', {'fields': ('status', 'rollout_percentage')}),
        ('Access Control', {'fields': ('require_staff', 'require_superuser', 'require_permissions')}),
        ('Scope', {'fields': ('environments', 'valid_from', 'valid_until')}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )