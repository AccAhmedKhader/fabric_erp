"""
Unit tests for authentication services.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from ..services.auth_service import AuthService
from ..services.user_service import UserService

User = get_user_model()


class AuthServiceTest(TestCase):
    """Test cases for AuthService."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            full_name='Test User',
            email='test@example.com',
            password='TestPassword123!'
        )

    def test_authenticate_success(self):
        """Test successful authentication."""
        request = self.factory.get('/login')
        success, user, error = AuthService.authenticate_user(
            'testuser', 'TestPassword123!', request
        )
        self.assertTrue(success)
        self.assertEqual(user, self.user)
        self.assertIsNone(error)

    def test_authenticate_invalid_password(self):
        """Test authentication with invalid password."""
        request = self.factory.get('/login')
        success, user, error = AuthService.authenticate_user(
            'testuser', 'WrongPassword', request
        )
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertEqual(error, 'Invalid username or password')

    def test_authenticate_inactive_user(self):
        """Test authentication with inactive user."""
        self.user.is_active = False
        self.user.save()

        request = self.factory.get('/login')
        success, user, error = AuthService.authenticate_user(
            'testuser', 'TestPassword123!', request
        )
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertEqual(error, 'Account is inactive. Please contact support.')

    def test_change_password_success(self):
        """Test successful password change."""
        success, message = AuthService.change_password(
            self.user, 'TestPassword123!', 'NewPassword123!'
        )
        self.assertTrue(success)
        self.assertEqual(message, 'Password changed successfully')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!'))

    def test_change_password_incorrect_current(self):
        """Test password change with incorrect current password."""
        success, message = AuthService.change_password(
            self.user, 'WrongPassword', 'NewPassword123!'
        )
        self.assertFalse(success)
        self.assertEqual(message, 'Current password is incorrect')


class UserServiceTest(TestCase):
    """Test cases for UserService."""

    def test_create_user_success(self):
        """Test successful user creation."""
        user_data = {
            'username': 'newuser',
            'full_name': 'New User',
            'email': 'new@example.com',
            'password': 'Password123!'
        }
        success, user, errors = UserService.create_user(user_data)
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.full_name, 'New User')
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('Password123!'))

    def test_create_user_duplicate_username(self):
        """Test user creation with duplicate username."""
        User.objects.create_user(
            username='existing',
            full_name='Existing User',
            email='existing@example.com',
            password='Password123!'
        )

        user_data = {
            'username': 'existing',
            'full_name': 'New User',
            'email': 'new@example.com',
            'password': 'Password123!'
        }
        success, user, errors = UserService.create_user(user_data)
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertIn('Username is already taken', errors)

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        User.objects.create_user(
            username='existing',
            full_name='Existing User',
            email='existing@example.com',
            password='Password123!'
        )

        user_data = {
            'username': 'newuser',
            'full_name': 'New User',
            'email': 'existing@example.com',
            'password': 'Password123!'
        }
        success, user, errors = UserService.create_user(user_data)
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertIn('Email is already registered', errors)

    def test_create_user_short_password(self):
        """Test user creation with short password."""
        user_data = {
            'username': 'newuser',
            'full_name': 'New User',
            'email': 'new@example.com',
            'password': '123'
        }
        success, user, errors = UserService.create_user(user_data)
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertIn('Password must be at least 8 characters', errors)