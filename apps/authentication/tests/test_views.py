"""
Unit tests for authentication views.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewsTest(TestCase):
    """Test cases for authentication views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            full_name='Test User',
            email='test@example.com',
            password='TestPassword123!'
        )

    def test_splash_view(self):
        """Test splash page."""
        response = self.client.get(reverse('authentication:splash'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'splash.html')

    def test_login_view_get(self):
        """Test login page GET."""
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        """Test successful login POST."""
        response = self.client.post(
            reverse('authentication:login'),
            {
                'username': 'testuser',
                'password': 'TestPassword123!'
            }
        )
        self.assertRedirects(response, reverse('authentication:dashboard'))

    def test_login_view_post_failure(self):
        """Test failed login POST."""
        response = self.client.post(
            reverse('authentication:login'),
            {
                'username': 'testuser',
                'password': 'WrongPassword'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password')

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication."""
        response = self.client.get(reverse('authentication:dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('authentication:login')}?next={reverse('authentication:dashboard')}"
        )

    def test_dashboard_authenticated(self):
        """Test dashboard with authenticated user."""
        self.client.login(username='testuser', password='TestPassword123!')
        response = self.client.get(reverse('authentication:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_logout(self):
        """Test logout functionality."""
        self.client.login(username='testuser', password='TestPassword123!')
        response = self.client.get(reverse('authentication:logout'))
        self.assertRedirects(response, reverse('authentication:login'))

    def test_forgot_password_get(self):
        """Test forgot password page GET."""
        response = self.client.get(reverse('authentication:forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')

    def test_forgot_password_post_valid_email(self):
        """Test forgot password with valid email."""
        response = self.client.post(
            reverse('authentication:forgot_password'),
            {'email': 'test@example.com'}
        )
        self.assertRedirects(response, reverse('authentication:login'))
        self.assertContains(response, 'Password reset link has been sent', status_code=302)

    def test_forgot_password_post_invalid_email(self):
        """Test forgot password with invalid email."""
        response = self.client.post(
            reverse('authentication:forgot_password'),
            {'email': 'nonexistent@example.com'}
        )
        self.assertRedirects(response, reverse('authentication:login'))
        self.assertContains(response, 'If an account exists, a reset link has been sent', status_code=302)