"""
Unit tests for authentication repositories.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..repositories.user_repository import UserRepository

User = get_user_model()


class UserRepositoryTest(TestCase):
    """Test cases for UserRepository."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            full_name='Test User',
            email='test@example.com',
            password='TestPassword123!'
        )

    def test_get_by_id(self):
        """Test getting user by ID."""
        found = UserRepository.get_by_id(self.user.id)
        self.assertEqual(found, self.user)

    def test_get_by_username(self):
        """Test getting user by username."""
        found = UserRepository.get_by_username('testuser')
        self.assertEqual(found, self.user)

    def test_get_by_email(self):
        """Test getting user by email."""
        found = UserRepository.get_by_email('test@example.com')
        self.assertEqual(found, self.user)

    def test_get_all(self):
        """Test getting all users."""
        users = UserRepository.get_all()
        self.assertIn(self.user, users)

    def test_get_all_with_search(self):
        """Test getting users with search filter."""
        User.objects.create_user(
            username='anotheruser',
            full_name='Another User',
            email='another@example.com',
            password='Password123!'
        )
        users = UserRepository.get_all(search='another')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().username, 'anotheruser')

    def test_authenticate_success(self):
        """Test successful authentication."""
        user = UserRepository.authenticate('testuser', 'TestPassword123!')
        self.assertEqual(user, self.user)

    def test_authenticate_failure(self):
        """Test failed authentication."""
        user = UserRepository.authenticate('testuser', 'WrongPassword')
        self.assertIsNone(user)

    def test_toggle_active(self):
        """Test toggling user active status."""
        user = UserRepository.toggle_active(self.user.id)
        self.assertFalse(user.is_active)

        user = UserRepository.toggle_active(self.user.id)
        self.assertTrue(user.is_active)

    def test_update_last_login(self):
        """Test updating last login."""
        self.assertIsNone(self.user.last_login)
        UserRepository.update_last_login(self.user)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)