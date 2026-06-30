"""
Service layer for authentication operations.
"""

import logging
from typing import Optional, Dict, Any, Tuple
from uuid import UUID
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ..models import LoginAudit, PasswordResetToken, EmailVerification, UserSession
from ..repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
User = get_user_model()


class AuthService:
    """
    Service class for handling authentication operations.
    """

    @staticmethod
    def authenticate_user(
        username: str,
        password: str,
        request: Any,
        remember_me: bool = False
    ) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Authenticate a user with username and password.

        Returns:
            Tuple of (success, user, error_message)
        """
        try:
            user = UserRepository.authenticate(username, password)

            if not user:
                AuthService._log_login_attempt(
                    username=username,
                    request=request,
                    success=False,
                    reason='Invalid credentials'
                )
                return False, None, 'Invalid username or password'

            if user.is_account_locked():
                AuthService._log_login_attempt(
                    user=user,
                    request=request,
                    success=False,
                    reason='Account locked'
                )
                return False, None, 'Account is locked. Please try again later.'

            if not user.is_active:
                AuthService._log_login_attempt(
                    user=user,
                    request=request,
                    success=False,
                    reason='Account inactive'
                )
                return False, None, 'Account is inactive. Please contact support.'

            user.reset_failed_attempts()
            UserRepository.update_last_login(user)
            AuthService._create_user_session(user, request)
            AuthService._log_login_attempt(
                user=user,
                request=request,
                success=True
            )

            login(request, user)

            if remember_me:
                request.session.set_expiry(settings.REMEMBER_ME_AGE)

            return True, user, None

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False, None, 'An error occurred during authentication'

    @staticmethod
    def logout_user(request: Any) -> None:
        """Logout a user and clean up session."""
        try:
            if request.user.is_authenticated:
                AuthService._log_logout(request.user, request)
                AuthService._terminate_user_session(request.user, request)

            logout(request)

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")

    @staticmethod
    def change_password(
        user: User,
        current_password: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Change user password.

        Returns:
            Tuple of (success, message)
        """
        try:
            if not user.check_password(current_password):
                return False, 'Current password is incorrect'

            user.set_password(new_password)
            user.save()

            logger.info(f"Password changed for user {user.username}")
            return True, 'Password changed successfully'

        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return False, 'An error occurred while changing password'

    @staticmethod
    def forgot_password(email: str, request: Any) -> Tuple[bool, str]:
        """
        Send password reset link to user's email.

        Returns:
            Tuple of (success, message)
        """
        try:
            user = UserRepository.get_by_email(email)
            if not user:
                return True, 'If an account exists, a reset link has been sent'

            token, raw_token = PasswordResetToken.generate_token(user)
            AuthService._send_reset_email(user, raw_token, request)

            logger.info(f"Password reset requested for {user.username}")
            return True, 'Password reset link has been sent to your email'

        except Exception as e:
            logger.error(f"Forgot password error: {str(e)}")
            return False, 'An error occurred while sending reset link'

    @staticmethod
    def reset_password(
        uidb64: str,
        token: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Reset password using token.

        Returns:
            Tuple of (success, message)
        """
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = UserRepository.get_by_id(UUID(user_id))

            if not user:
                return False, 'Invalid reset link'

            reset_token = PasswordResetToken.objects.filter(
                user=user,
                is_used=False
            ).first()

            if not reset_token or not reset_token.is_valid():
                return False, 'Invalid or expired reset link'

            if reset_token.token != token:
                return False, 'Invalid reset link'

            user.set_password(new_password)
            user.save()

            reset_token.mark_as_used()

            logger.info(f"Password reset successful for {user.username}")
            return True, 'Password reset successfully'

        except Exception as e:
            logger.error(f"Reset password error: {str(e)}")
            return False, 'An error occurred while resetting password'

    @staticmethod
    def verify_email(uidb64: str, token: str) -> Tuple[bool, str]:
        """
        Verify user's email address.

        Returns:
            Tuple of (success, message)
        """
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = UserRepository.get_by_id(UUID(user_id))

            if not user:
                return False, 'Invalid verification link'

            verification = EmailVerification.objects.filter(
                user=user,
                is_verified=False
            ).first()

            if not verification or not verification.is_valid():
                return False, 'Invalid or expired verification link'

            if verification.token != token:
                return False, 'Invalid verification link'

            verification.verify_email()

            logger.info(f"Email verified for {user.username}")
            return True, 'Email verified successfully'

        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            return False, 'An error occurred while verifying email'

    @staticmethod
    def resend_verification(email: str, request: Any) -> Tuple[bool, str]:
        """
        Resend email verification link.

        Returns:
            Tuple of (success, message)
        """
        try:
            user = UserRepository.get_by_email(email)
            if not user or user.is_email_verified:
                return False, 'Email is already verified or account does not exist'

            verification, raw_token = EmailVerification.generate_token(user)
            AuthService._send_verification_email(user, raw_token, request)

            logger.info(f"Verification email resent for {user.username}")
            return True, 'Verification email has been sent'

        except Exception as e:
            logger.error(f"Resend verification error: {str(e)}")
            return False, 'An error occurred while sending verification email'

    @staticmethod
    def _log_login_attempt(
        user: Optional[User] = None,
        username: Optional[str] = None,
        request: Any = None,
        success: bool = True,
        reason: str = ''
    ) -> None:
        """Log a login attempt."""
        try:
            login_audit = LoginAudit(
                user=user,
                username=username or (user.username if user else 'unknown'),
                status=LoginAudit.LoginStatus.SUCCESS if success else LoginAudit.LoginStatus.FAILURE,
                failure_reason=reason if not success else '',
                ip_address=request.META.get('REMOTE_ADDR') if request else None,
                user_agent=request.META.get('HTTP_USER_AGENT') if request else '',
                browser=AuthService._detect_browser(request),
                device=AuthService._detect_device(request),
            )
            login_audit.save()

            audit_logger = logging.getLogger('audit')
            audit_logger.info(
                f"Login {'success' if success else 'failure'} - User: {login_audit.username} - "
                f"IP: {login_audit.ip_address} - Reason: {reason}"
            )

        except Exception as e:
            logger.error(f"Error logging login attempt: {str(e)}")

    @staticmethod
    def _log_logout(user: User, request: Any) -> None:
        """Log a logout event."""
        try:
            login_audit = LoginAudit.objects.filter(
                user=user,
                session_key=request.session.session_key
            ).order_by('-login_time').first()

            if login_audit:
                login_audit.set_logout()

            audit_logger = logging.getLogger('audit')
            audit_logger.info(
                f"Logout - User: {user.username} - IP: {request.META.get('REMOTE_ADDR')}"
            )

        except Exception as e:
            logger.error(f"Error logging logout: {str(e)}")

    @staticmethod
    def _create_user_session(user: User, request: Any) -> None:
        """Create a user session record."""
        try:
            session = UserSession.objects.create(
                user=user,
                session_key=request.session.session_key,
                expires_at=timezone.now() + timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                browser=AuthService._detect_browser(request),
                device=AuthService._detect_device(request),
            )
            return session
        except Exception as e:
            logger.error(f"Error creating user session: {str(e)}")
            return None

    @staticmethod
    def _terminate_user_session(user: User, request: Any) -> None:
        """Terminate a user session."""
        try:
            session = UserSession.objects.filter(
                user=user,
                session_key=request.session.session_key
            ).first()

            if session:
                session.terminate()

        except Exception as e:
            logger.error(f"Error terminating user session: {str(e)}")

    @staticmethod
    def _send_reset_email(user: User, token: str, request: Any) -> None:
        """Send password reset email."""
        try:
            uid = urlsafe_base64_encode(force_bytes(str(user.id)))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            context = {
                'user': user,
                'reset_link': reset_link,
                'site_name': settings.COMPANY_NAME,
            }

            subject = f"Password Reset - {settings.COMPANY_NAME}"
            message = render_to_string('emails/password_reset.html', context)

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )

            logger.info(f"Reset email sent to {user.email}")

        except Exception as e:
            logger.error(f"Error sending reset email: {str(e)}")
            raise

    @staticmethod
    def _send_verification_email(user: User, token: str, request: Any) -> None:
        """Send email verification email."""
        try:
            uid = urlsafe_base64_encode(force_bytes(str(user.id)))
            verification_link = f"{request.scheme}://{request.get_host()}/verify-email/{uid}/{token}/"

            context = {
                'user': user,
                'verification_link': verification_link,
                'site_name': settings.COMPANY_NAME,
            }

            subject = f"Verify Your Email - {settings.COMPANY_NAME}"
            message = render_to_string('emails/email_verification.html', context)

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )

            logger.info(f"Verification email sent to {user.email}")

        except Exception as e:
            logger.error(f"Error sending verification email: {str(e)}")
            raise

    @staticmethod
    def _detect_browser(request: Any) -> str:
        """Detect browser from user agent."""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'chrome' in user_agent:
            return 'Chrome'
        elif 'firefox' in user_agent:
            return 'Firefox'
        elif 'safari' in user_agent and 'chrome' not in user_agent:
            return 'Safari'
        elif 'edge' in user_agent:
            return 'Edge'
        elif 'opera' in user_agent:
            return 'Opera'
        else:
            return 'Other'

    @staticmethod
    def _detect_device(request: Any) -> str:
        """Detect device from user agent."""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            return 'Mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'Tablet'
        else:
            return 'Desktop'