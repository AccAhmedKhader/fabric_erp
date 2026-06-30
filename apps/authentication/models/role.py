"""
Role model definition for FabricERP.
Uses One-to-One relationship with Django's Group instead of inheritance.
"""

import uuid
from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class Role(models.Model):
    """
    Enhanced Role model that links to Django's Group via OneToOneField.
    """
    class Meta:
        db_table = 'auth_roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for the role'
    )

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='role',
        help_text='Linked Django group'
    )

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text='Role name (matches group name)'
    )

    description = models.TextField(
        blank=True,
        help_text='Description of the role and its permissions'
    )

    is_system = models.BooleanField(
        default=False,
        help_text='Whether this is a system role that cannot be deleted'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time when role was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Date and time when role was last updated'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save to handle group creation and synchronization."""
        if not self.pk:
            # Create or get matching group
            group, created = Group.objects.get_or_create(name=self.name)
            self.group = group
        else:
            # Sync group name if role name changed
            if hasattr(self, 'group') and self.group and self.group.name != self.name:
                self.group.name = self.name
                self.group.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to handle group deletion."""
        if self.is_system:
            raise ValidationError('System roles cannot be deleted.')
        group = self.group
        super().delete(*args, **kwargs)
        if group:
            group.delete()

    @classmethod
    def create_system_roles(cls):
        """Create default system roles."""
        system_roles = [
            {
                'name': 'System Administrator',
                'description': 'Full system access with all permissions',
                'is_system': True,
            },
            {
                'name': 'Accountant',
                'description': 'Access to accounting modules and financial data',
                'is_system': True,
            },
            {
                'name': 'Sales Manager',
                'description': 'Access to sales modules and reporting',
                'is_system': True,
            },
            {
                'name': 'Inventory Manager',
                'description': 'Access to inventory and warehouse modules',
                'is_system': True,
            },
            {
                'name': 'Purchasing Manager',
                'description': 'Access to purchasing and procurement modules',
                'is_system': True,
            },
            {
                'name': 'HR Manager',
                'description': 'Access to human resources modules',
                'is_system': True,
            },
            {
                'name': 'User',
                'description': 'Basic user access with limited permissions',
                'is_system': True,
            },
        ]

        for role_data in system_roles:
            # Create or get group first
            group, group_created = Group.objects.get_or_create(name=role_data['name'])
            
            # Create or get role with the group
            role, role_created = cls.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'group': group,
                    'description': role_data['description'],
                    'is_system': role_data['is_system'],
                }
            )
            
            if not role_created:
                # Update existing role if needed
                role.description = role_data['description']
                role.is_system = role_data['is_system']
                role.save()