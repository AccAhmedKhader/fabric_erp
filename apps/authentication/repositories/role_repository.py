"""
Repository pattern implementation for Role model.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet
from ..models import Role, EnterprisePermission


class RoleRepository:
    """
    Repository for Role model operations.
    """

    @staticmethod
    def get_by_id(role_id: UUID) -> Optional[Role]:
        """Get a role by UUID."""
        try:
            return Role.objects.get(id=role_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_name(name: str) -> Optional[Role]:
        """Get a role by name."""
        try:
            return Role.objects.get(name__iexact=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all(
        search: Optional[str] = None,
        is_system: Optional[bool] = None,
        order_by: str = 'name'
    ) -> QuerySet:
        """Get all roles with optional filters."""
        queryset = Role.objects.all()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if is_system is not None:
            queryset = queryset.filter(is_system=is_system)

        return queryset.order_by(order_by)

    @staticmethod
    @transaction.atomic
    def create(role_data: Dict[str, Any]) -> Role:
        """Create a new role."""
        role = Role(**role_data)
        role.save()
        return role

    @staticmethod
    @transaction.atomic
    def update(role_id: UUID, role_data: Dict[str, Any]) -> Optional[Role]:
        """Update an existing role."""
        role = RoleRepository.get_by_id(role_id)
        if not role:
            return None

        # Don't allow updating system role name
        if role.is_system:
            role_data.pop('name', None)

        for key, value in role_data.items():
            setattr(role, key, value)

        role.save()
        return role

    @staticmethod
    @transaction.atomic
    def delete(role_id: UUID) -> bool:
        """Delete a role."""
        role = RoleRepository.get_by_id(role_id)
        if not role or role.is_system:
            return False
        role.delete()
        return True

    @staticmethod
    @transaction.atomic
    def assign_permissions(role_id: UUID, permission_ids: List[UUID]) -> Optional[Role]:
        """Assign permissions to a role."""
        role = RoleRepository.get_by_id(role_id)
        if not role:
            return None

        permissions = EnterprisePermission.objects.filter(id__in=permission_ids)
        role.enterprise_permissions.set(permissions)
        return role

    @staticmethod
    def get_permissions(role_id: UUID) -> QuerySet:
        """Get all permissions assigned to a role."""
        role = RoleRepository.get_by_id(role_id)
        if not role:
            return EnterprisePermission.objects.none()
        return role.enterprise_permissions.all()

    @staticmethod
    def get_users(role_id: UUID) -> QuerySet:
        """Get all users with this role."""
        from ..models import User
        role = RoleRepository.get_by_id(role_id)
        if not role:
            return User.objects.none()
        return role.user_set.all()