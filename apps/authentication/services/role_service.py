"""
Service layer for role management operations.
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from django.db import transaction
from ..repositories.role_repository import RoleRepository
from ..repositories.permission_repository import PermissionRepository

logger = logging.getLogger(__name__)


class RoleService:
    """
    Service class for handling role management operations.
    """

    @staticmethod
    def create_role(role_data: Dict[str, Any]) -> Tuple[bool, Optional[Any], List[str]]:
        """
        Create a new role.

        Returns:
            Tuple of (success, role, errors)
        """
        errors = []

        try:
            if RoleRepository.get_by_name(role_data.get('name', '')):
                errors.append('Role name is already taken')

            if errors:
                return False, None, errors

            role = RoleRepository.create(role_data)
            logger.info(f"Role created: {role.name}")
            return True, role, []

        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return False, None, [str(e)]

    @staticmethod
    def update_role(role_id: UUID, role_data: Dict[str, Any]) -> Tuple[bool, Optional[Any], List[str]]:
        """
        Update an existing role.

        Returns:
            Tuple of (success, role, errors)
        """
        errors = []

        try:
            role = RoleRepository.get_by_id(role_id)
            if not role:
                return False, None, ['Role not found']

            if role.is_system:
                errors.append('System roles cannot be modified')

            name = role_data.get('name')
            if name and name != role.name:
                if RoleRepository.get_by_name(name):
                    errors.append('Role name is already taken')

            if errors:
                return False, None, errors

            role = RoleRepository.update(role_id, role_data)
            logger.info(f"Role updated: {role.name}")
            return True, role, []

        except Exception as e:
            logger.error(f"Error updating role: {str(e)}")
            return False, None, [str(e)]

    @staticmethod
    def delete_role(role_id: UUID) -> Tuple[bool, str]:
        """
        Delete a role.

        Returns:
            Tuple of (success, message)
        """
        try:
            role = RoleRepository.get_by_id(role_id)
            if not role:
                return False, 'Role not found'

            if role.is_system:
                return False, 'System roles cannot be deleted'

            RoleRepository.delete(role_id)
            logger.info(f"Role deleted: {role.name}")
            return True, 'Role deleted successfully'

        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return False, str(e)

    @staticmethod
    def assign_permissions(role_id: UUID, permission_ids: List[UUID]) -> Tuple[bool, str]:
        """
        Assign permissions to a role.

        Returns:
            Tuple of (success, message)
        """
        try:
            role = RoleRepository.get_by_id(role_id)
            if not role:
                return False, 'Role not found'

            permissions = PermissionRepository.get_all()
            valid_permission_ids = set(permissions.values_list('id', flat=True))

            valid_ids = [pid for pid in permission_ids if pid in valid_permission_ids]

            if not valid_ids:
                return False, 'No valid permissions selected'

            RoleRepository.assign_permissions(role_id, valid_ids)
            logger.info(f"Permissions assigned to role: {role.name}")
            return True, 'Permissions assigned successfully'

        except Exception as e:
            logger.error(f"Error assigning permissions: {str(e)}")
            return False, str(e)