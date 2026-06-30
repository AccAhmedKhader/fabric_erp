"""
Service layer for user management operations.
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from django.db import transaction
from django.contrib.auth import get_user_model
from ..repositories.user_repository import UserRepository
from ..repositories.role_repository import RoleRepository

logger = logging.getLogger(__name__)
User = get_user_model()


class UserService:
    """
    Service class for handling user management operations.
    """

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Tuple[bool, Optional[User], List[str]]:
        """
        Create a new user.

        Returns:
            Tuple of (success, user, errors)
        """
        errors = []

        try:
            if UserRepository.get_by_email(user_data.get('email', '')):
                errors.append('Email is already registered')

            if UserRepository.get_by_username(user_data.get('username', '')):
                errors.append('Username is already taken')

            password = user_data.get('password')
            if not password or len(password) < 8:
                errors.append('Password must be at least 8 characters')

            if errors:
                return False, None, errors

            user = UserRepository.create(user_data)

            logger.info(f"User created: {user.username}")
            return True, user, []

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return False, None, [str(e)]

    @staticmethod
    def update_user(user_id: UUID, user_data: Dict[str, Any]) -> Tuple[bool, Optional[User], List[str]]:
        """
        Update an existing user.

        Returns:
            Tuple of (success, user, errors)
        """
        errors = []

        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                return False, None, ['User not found']

            email = user_data.get('email')
            if email and email != user.email:
                if UserRepository.get_by_email(email):
                    errors.append('Email is already registered')

            username = user_data.get('username')
            if username and username != user.username:
                if UserRepository.get_by_username(username):
                    errors.append('Username is already taken')

            if errors:
                return False, None, errors

            user = UserRepository.update(user_id, user_data)

            logger.info(f"User updated: {user.username}")
            return True, user, []

        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return False, None, [str(e)]

    @staticmethod
    def delete_user(user_id: UUID) -> Tuple[bool, str]:
        """
        Delete a user.

        Returns:
            Tuple of (success, message)
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                return False, 'User not found'

            if user.is_superuser:
                superuser_count = User.objects.filter(is_superuser=True).count()
                if superuser_count <= 1:
                    return False, 'Cannot delete the last superuser'

            UserRepository.delete(user_id)
            logger.info(f"User deleted: {user.username}")
            return True, 'User deleted successfully'

        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return False, str(e)

    @staticmethod
    def toggle_user_active(user_id: UUID) -> Tuple[bool, Optional[User], str]:
        """
        Toggle user active status.

        Returns:
            Tuple of (success, user, message)
        """
        try:
            user = UserRepository.toggle_active(user_id)
            if not user:
                return False, None, 'User not found'

            status = 'activated' if user.is_active else 'deactivated'
            logger.info(f"User {status}: {user.username}")
            return True, user, f'User {status} successfully'

        except Exception as e:
            logger.error(f"Error toggling user status: {str(e)}")
            return False, None, str(e)

    @staticmethod
    def assign_role(user_id: UUID, role_id: UUID) -> Tuple[bool, str]:
        """
        Assign a role to a user.

        Returns:
            Tuple of (success, message)
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                return False, 'User not found'

            role = RoleRepository.get_by_id(role_id)
            if not role:
                return False, 'Role not found'

            user.groups.add(role)
            logger.info(f"Role {role.name} assigned to user {user.username}")
            return True, f'Role {role.name} assigned successfully'

        except Exception as e:
            logger.error(f"Error assigning role: {str(e)}")
            return False, str(e)

    @staticmethod
    def remove_role(user_id: UUID, role_id: UUID) -> Tuple[bool, str]:
        """
        Remove a role from a user.

        Returns:
            Tuple of (success, message)
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                return False, 'User not found'

            role = RoleRepository.get_by_id(role_id)
            if not role:
                return False, 'Role not found'

            user.groups.remove(role)
            logger.info(f"Role {role.name} removed from user {user.username}")
            return True, f'Role {role.name} removed successfully'

        except Exception as e:
            logger.error(f"Error removing role: {str(e)}")
            return False, str(e)