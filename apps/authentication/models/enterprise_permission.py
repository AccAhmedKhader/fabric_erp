"""
Enterprise permission system that extends Django's built-in permissions
without modifying the core Permission model.
"""

import uuid
from django.db import models
from django.contrib.auth.models import Permission as DjangoPermission
from django.contrib.contenttypes.models import ContentType


class PermissionCategory(models.Model):
    """
    Categories for organizing permissions in the enterprise system.
    """
    class Meta:
        db_table = 'auth_permission_categories'
        verbose_name = 'Permission Category'
        verbose_name_plural = 'Permission Categories'
        ordering = ['order', 'name']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Category name (e.g., Accounting, Inventory, Sales)'
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique category code'
    )

    description = models.TextField(
        blank=True,
        help_text='Category description'
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='CSS icon class'
    )

    order = models.IntegerField(
        default=0,
        help_text='Display order'
    )

    is_system = models.BooleanField(
        default=False,
        help_text='Whether this is a system category'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text='Parent category'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Get the full category path."""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class EnterprisePermission(models.Model):
    """
    Enterprise permission that extends Django's built-in permission.
    Uses a one-to-one relationship with Django's Permission.
    """
    class Meta:
        db_table = 'auth_enterprise_permissions'
        verbose_name = 'Enterprise Permission'
        verbose_name_plural = 'Enterprise Permissions'
        ordering = ['category__order', 'django_permission__codename']

    class PermissionType(models.TextChoices):
        VIEW = 'view', 'View'
        CREATE = 'create', 'Create'
        EDIT = 'edit', 'Edit'
        DELETE = 'delete', 'Delete'
        APPROVE = 'approve', 'Approve'
        REJECT = 'reject', 'Reject'
        EXPORT = 'export', 'Export'
        IMPORT = 'import', 'Import'
        ADMIN = 'admin', 'Administrate'
        FULL = 'full', 'Full Access'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    django_permission = models.OneToOneField(
        DjangoPermission,
        on_delete=models.CASCADE,
        related_name='enterprise_permission',
        help_text='Linked Django permission'
    )

    category = models.ForeignKey(
        PermissionCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permissions',
        help_text='Permission category'
    )

    permission_type = models.CharField(
        max_length=20,
        choices=PermissionType.choices,
        default=PermissionType.VIEW,
        help_text='Type of permission'
    )

    is_enterprise = models.BooleanField(
        default=True,
        help_text='Whether this is an enterprise permission'
    )

    is_system = models.BooleanField(
        default=False,
        help_text='Whether this is a system permission that cannot be deleted'
    )

    description = models.TextField(
        blank=True,
        help_text='Detailed description of the permission'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.django_permission.codename} ({self.category.name if self.category else 'Uncategorized'})"

    @property
    def codename(self):
        """Get the permission codename."""
        return self.django_permission.codename

    @property
    def name(self):
        """Get the permission name."""
        return self.django_permission.name

    @classmethod
    def create_enterprise_permission(cls, codename, name, category_code, permission_type='view', **kwargs):
        """
        Create an enterprise permission linked to a Django permission.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()

        content_type = ContentType.objects.get_for_model(User)

        django_perm, created = DjangoPermission.objects.get_or_create(
            codename=codename,
            content_type=content_type,
            defaults={'name': name}
        )

        if created:
            django_perm.name = name
            django_perm.save()

        category = PermissionCategory.objects.filter(code=category_code).first()

        enterprise_perm, created = cls.objects.get_or_create(
            django_permission=django_perm,
            defaults={
                'category': category,
                'permission_type': permission_type,
                'description': kwargs.get('description', ''),
                'is_system': kwargs.get('is_system', False),
            }
        )

        return enterprise_perm

    @classmethod
    def create_system_permissions(cls):
        """Create all system permissions."""
        permissions_data = [
            {
                'codename': 'view_dashboard',
                'name': 'Can view dashboard',
                'category': 'auth',
                'permission_type': 'view',
                'description': 'Access to the main dashboard'
            },
            {
                'codename': 'view_audit_log',
                'name': 'Can view audit log',
                'category': 'auth',
                'permission_type': 'view',
                'description': 'Access to audit logs'
            },
            {
                'codename': 'manage_users',
                'name': 'Can manage users',
                'category': 'auth',
                'permission_type': 'admin',
                'description': 'Full user management'
            },
            {
                'codename': 'manage_roles',
                'name': 'Can manage roles',
                'category': 'auth',
                'permission_type': 'admin',
                'description': 'Full role management'
            },
            {
                'codename': 'manage_permissions',
                'name': 'Can manage permissions',
                'category': 'auth',
                'permission_type': 'admin',
                'description': 'Full permission management'
            },
            {
                'codename': 'view_system_settings',
                'name': 'Can view system settings',
                'category': 'settings',
                'permission_type': 'view',
                'description': 'View system configuration'
            },
            {
                'codename': 'manage_system_settings',
                'name': 'Can manage system settings',
                'category': 'settings',
                'permission_type': 'admin',
                'description': 'Full system configuration'
            },
            {
                'codename': 'view_companies',
                'name': 'Can view companies',
                'category': 'company',
                'permission_type': 'view',
                'description': 'View company information'
            },
            {
                'codename': 'manage_companies',
                'name': 'Can manage companies',
                'category': 'company',
                'permission_type': 'admin',
                'description': 'Full company management'
            },
            {
                'codename': 'view_branches',
                'name': 'Can view branches',
                'category': 'company',
                'permission_type': 'view',
                'description': 'View branch information'
            },
            {
                'codename': 'manage_branches',
                'name': 'Can manage branches',
                'category': 'company',
                'permission_type': 'admin',
                'description': 'Full branch management'
            },
        ]

        for perm_data in permissions_data:
            cls.create_enterprise_permission(
                codename=perm_data['codename'],
                name=perm_data['name'],
                category_code=perm_data['category'],
                permission_type=perm_data['permission_type'],
                description=perm_data.get('description', ''),
                is_system=True
            )


class RoleEnterprisePermission(models.Model):
    """
    Many-to-many relationship between Roles and Enterprise Permissions.
    Extends Django's built-in group permissions.
    """
    class Meta:
        db_table = 'auth_role_enterprise_permissions'
        verbose_name = 'Role Enterprise Permission'
        verbose_name_plural = 'Role Enterprise Permissions'
        unique_together = [['role', 'enterprise_permission']]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    role = models.ForeignKey(
        'authentication.Role',
        on_delete=models.CASCADE,
        related_name='enterprise_permissions'
    )

    enterprise_permission = models.ForeignKey(
        EnterprisePermission,
        on_delete=models.CASCADE,
        related_name='assigned_roles'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    assigned_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_role_permissions'
    )

    def __str__(self):
        return f"{self.role.name} - {self.enterprise_permission.codename}"