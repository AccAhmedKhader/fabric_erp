"""
Health check views for monitoring and orchestration.
"""

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint.
    Returns 200 OK if the application is healthy.
    """
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': getattr(settings, 'APP_VERSION', '1.0.0'),
        'environment': getattr(settings, 'ENVIRONMENT', 'development'),
    }
    return JsonResponse(status, status=200)


def readiness_check(request):
    """
    Readiness check endpoint.
    Verifies that all dependencies are ready.
    """
    status = {
        'status': 'ready',
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    is_ready = True

    # Check database
    try:
        db_conn = connections['default']
        db_conn.cursor()
        status['checks']['database'] = {'status': 'ok'}
    except OperationalError as e:
        status['checks']['database'] = {'status': 'error', 'message': str(e)}
        is_ready = False

    # Check Redis if configured (with error handling)
    if hasattr(settings, 'REDIS_URL') and settings.REDIS_URL:
        try:
            import redis
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.ping()
            status['checks']['redis'] = {'status': 'ok'}
        except ImportError:
            status['checks']['redis'] = {'status': 'skipped', 'message': 'Redis library not installed'}
        except Exception as e:
            status['checks']['redis'] = {'status': 'error', 'message': str(e)}
            is_ready = False

    status['status'] = 'ready' if is_ready else 'not_ready'
    http_status = 200 if is_ready else 503

    return JsonResponse(status, status=http_status)


def liveness_check(request):
    """
    Liveness check endpoint for Kubernetes.
    Returns 200 OK if the application is alive.
    """
    status = {
        'status': 'alive',
        'timestamp': datetime.now().isoformat(),
    }
    return JsonResponse(status, status=200)


def metrics(request):
    """
    Simple metrics endpoint for monitoring.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    metrics_data = {
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'staff_users': User.objects.filter(is_staff=True).count(),
            'superusers': User.objects.filter(is_superuser=True).count(),
            'verified_emails': User.objects.filter(is_email_verified=True).count(),
        }
    }

    return JsonResponse(metrics_data, status=200)