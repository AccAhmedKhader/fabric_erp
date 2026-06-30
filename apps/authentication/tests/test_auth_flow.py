"""
End-to-end authentication flow tests.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthFlowTest(TestCase):
    """Test cases for end-to-end authentication flow."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='flowuser',
            full_name='Flow User',
            email='flow@example.com',
            password='FlowPassword123!'
        )

    def test_full_login_logout_flow(self):
        """Test complete login and logout flow."""
        # Login
        login_response = self.client.post(
            reverse('authentication:login'),
            {'username': 'flowuser', 'password': 'FlowPassword123!'}
        )
        self.assertRedirects(login_response, reverse('authentication:dashboard'))

        # Access dashboard
        dashboard_response = self.client.get(reverse('authentication:dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)

        # Logout
        logout_response = self.client.get(reverse('authentication:logout'))
        self.assertRedirects(logout_response, reverse('authentication:login'))

        # Dashboard should be inaccessible after logout
        dashboard_after_logout = self.client.get(reverse('authentication:dashboard'))
        self.assertRedirects(
            dashboard_after_logout,
            f"{reverse('authentication:login')}?next={reverse('authentication:dashboard')}"
        )

    def test_failed_login_locks_account(self):
        """Test that failed login attempts lock the account."""
        for i in range(5):
            response = self.client.post(
                reverse('authentication:login'),
                {'username': 'flowuser', 'password': 'WrongPassword'}
            )
            self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_account_locked())

        # Even with correct password, account remains locked
        response = self.client.post(
            reverse('authentication:login'),
            {'username': 'flowuser', 'password': 'FlowPassword123!'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account is locked')

    def test_remember_me_functionality(self):
        """Test remember me functionality."""
        response = self.client.post(
            reverse('authentication:login'),
            {
                'username': 'flowuser',
                'password': 'FlowPassword123!',
                'remember_me': True
            }
        )
        self.assertRedirects(response, reverse('authentication:dashboard'))

        # Check that session expiry is extended
        self.assertIsNotNone(self.client.session.get_expiry_age())
        self.assertGreater(self.client.session.get_expiry_age(), 3600)

    def test_password_reset_flow(self):
        """Test complete password reset flow."""
        # Request password reset
        response = self.client.post(
            reverse('authentication:forgot_password'),
            {'email': 'flow@example.com'}
        )
        self.assertRedirects(response, reverse('authentication:login'))

        # In production, this would send an email with a reset link
        # For testing, we verify the token was created
        from ..models import PasswordResetToken
        token = PasswordResetToken.objects.filter(user=self.user).first()
        self.assertIsNotNone(token)
        self.assertFalse(token.is_used)
        self.assertTrue(token.is_valid())