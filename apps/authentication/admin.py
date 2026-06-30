"""
Admin configuration for authentication app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Role, EnterprisePermission, PermissionCategory, UserProfile,
    LoginAudit, PasswordResetToken, EmailVerification, UserSession
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with enhanced display and filtering.
    """
    list_display = (
        'username', 'full_name', 'email', 'phone',
        'is_active', 'is_staff', 'is_email_verified',
        'created_at', 'last_login'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser',
        'is_email_verified', 'is_deleted', 'created_at'
    )
    search_fields = ('username', 'full_name', 'email', 'phone')
    readonly_fields = (
        'created_at', 'updated_at', 'last_login',
        'failed_login_attempts', 'locked_until',
        'email_verified_at', 'last_password_change'
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Security'), {'fields': ('is_email_verified', 'email_verified_at', 'failed_login_attempts', 'locked_until', 'last_password_change', 'is_2fa_enabled')}),
        (_('Status'), {'fields': ('is_deleted', 'deleted_at', 'deleted_by')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ('-created_at',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Role admin configuration.
    """
    list_display = ('name', 'description', 'is_system', 'created_at')
    list_filter = ('is_system', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_system')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(EnterprisePermission)
class EnterprisePermissionAdmin(admin.ModelAdmin):
    """
    Enterprise permission admin configuration.
    """
    list_display = ('codename', 'name', 'category', 'permission_type', 'is_system')
    list_filter = ('category', 'permission_type', 'is_system', 'created_at')
    search_fields = ('django_permission__codename', 'django_permission__name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PermissionCategory)
class PermissionCategoryAdmin(admin.ModelAdmin):
    """
    Permission category admin configuration.
    """
    list_display = ('name', 'code', 'order', 'is_system')
    list_filter = ('is_system', 'created_at')
    search_fields = ('name', 'code', 'description')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User profile admin configuration.
    """
    list_display = ('user', 'department', 'job_title', 'language', 'theme')
    list_filter = ('department', 'language', 'theme')
    search_fields = ('user__username', 'user__full_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Personal Information'), {'fields': ('avatar', 'date_of_birth', 'gender', 'nationality')}),
        (_('Professional Information'), {'fields': ('department', 'job_title', 'employee_id', 'manager', 'hire_date')}),
        (_('Preferences'), {'fields': ('language', 'theme', 'timezone')}),
        (_('Notifications'), {'fields': ('email_notifications', 'push_notifications')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    """
    Login audit admin configuration.
    """
    list_display = ('username', 'login_time', 'status', 'ip_address', 'browser', 'device')
    list_filter = ('status', 'login_time', 'browser')
    search_fields = ('username', 'ip_address', 'user_agent')
    readonly_fields = (
        'id', 'user', 'username', 'login_time', 'logout_time',
        'ip_address', 'user_agent', 'browser', 'device',
        'status', 'failure_reason', 'session_key'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Password reset token admin configuration.
    """
    list_display = ('user', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
        'id', 'user', 'token', 'created_at',
        'expires_at', 'ip_address', 'user_agent'
    )

    def has_add_permission(self, request):
        return False


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Email verification admin configuration.
    """
    list_display = ('user', 'created_at', 'expires_at', 'is_verified')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
        'id', 'user', 'token', 'created_at',
        'expires_at', 'ip_address', 'user_agent'
    )

    def has_add_permission(self, request):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    User session admin configuration.
    """
    list_display = ('user', 'session_key', 'created_at', 'expires_at', 'is_active', 'last_activity')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = (
        'id', 'user', 'session_key', 'created_at',
        'expires_at', 'ip_address', 'user_agent',
        'browser', 'device', 'last_activity'
    )

    def has_add_permission(self, request):
        return False