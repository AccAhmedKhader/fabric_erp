"""
Unit tests for authentication models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from uuid import UUID
from ..models import User, Role, UserProfile

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
        }

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPassword123!'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsInstance(user.id, UUID)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            username='admin',
            full_name='Admin User',
            email='admin@example.com',
            password='AdminPassword123!'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'Test User (testuser)')

    def test_user_get_full_name(self):
        """Test get full name method."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_user_account_lock(self):
        """Test account locking functionality."""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_account_locked())

        user.lock_account(duration_minutes=30)
        self.assertTrue(user.is_account_locked())

        user.unlock_account()
        self.assertFalse(user.is_account_locked())

    def test_failed_login_attempts(self):
        """Test failed login attempts tracking."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.failed_login_attempts, 0)

        user.increment_failed_attempts()
        self.assertEqual(user.failed_login_attempts, 1)

        user.reset_failed_attempts()
        self.assertEqual(user.failed_login_attempts, 0)

    def test_email_verification(self):
        """Test email verification functionality."""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_email_verified)
        self.assertIsNone(user.email_verified_at)

        user.verify_email()
        self.assertTrue(user.is_email_verified)
        self.assertIsNotNone(user.email_verified_at)


class RoleModelTest(TestCase):
    """Test cases for Role model."""

    def setUp(self):
        """Set up test data."""
        self.role_data = {
            'name': 'Test Role',
            'description': 'A test role',
        }

    def test_create_role(self):
        """Test creating a role."""
        role = Role.objects.create(**self.role_data)
        self.assertIsInstance(role, Role)
        self.assertEqual(role.name, 'Test Role')
        self.assertEqual(role.description, 'A test role')
        self.assertFalse(role.is_system)
        self.assertIsInstance(role.id, UUID)

    def test_create_system_role(self):
        """Test creating a system role."""
        role = Role.objects.create(
            name='System Role',
            description='System role',
            is_system=True
        )
        self.assertTrue(role.is_system)

    def test_role_str(self):
        """Test role string representation."""
        role = Role.objects.create(**self.role_data)
        self.assertEqual(str(role), 'Test Role')


class UserProfileTest(TestCase):
    """Test cases for UserProfile model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='profileuser',
            full_name='Profile User',
            email='profile@example.com',
            password='Password123!'
        )

    def test_profile_created_signal(self):
        """Test that profile is automatically created."""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user, self.user)

    def test_profile_str(self):
        """Test profile string representation."""
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'Profile for profileuser')

    def test_profile_preferences(self):
        """Test profile preferences."""
        profile = UserProfile.objects.get(user=self.user)
        profile.language = UserProfile.Language.ARABIC
        profile.theme = UserProfile.Theme.DARK
        profile.save()

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.language, 'ar')
        self.assertEqual(updated_profile.theme, 'dark')