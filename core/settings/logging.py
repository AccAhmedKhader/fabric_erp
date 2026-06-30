"""
Enterprise logging configuration with separate log files.
"""

import os
from pathlib import Path

# Ensure logs directory exists
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
APP_LOG = str(LOGS_DIR / 'application.log')
SECURITY_LOG = str(LOGS_DIR / 'security.log')
AUDIT_LOG = str(LOGS_DIR / 'audit.log')
ERROR_LOG = str(LOGS_DIR / 'errors.log')
PERFORMANCE_LOG = str(LOGS_DIR / 'performance.log')
DB_LOG = str(LOGS_DIR / 'database.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name} {module}.{funcName}:{lineno} - {message}',
            'style': '{',
        },
        'audit': {
            'format': '{asctime} [AUDIT] {message}',
            'style': '{',
        },
        'security': {
            'format': '{asctime} [SECURITY] {levelname} {name} - {message}',
            'style': '{',
        },
        'error': {
            'format': '{asctime} [ERROR] {name} {module}.{funcName}:{lineno} - {message}\n{exc_info}',
            'style': '{',
        },
        'performance': {
            'format': '{asctime} [PERF] {name} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },

    'handlers': {
        # Application logs
        'app_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': APP_LOG,
            'maxBytes': 10485760,  # 10MB
            'backupCount': 30,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        # Security logs
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SECURITY_LOG,
            'maxBytes': 10485760,
            'backupCount': 30,
            'formatter': 'security',
            'level': 'INFO',
        },
        # Audit logs
        'audit_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': AUDIT_LOG,
            'maxBytes': 10485760,
            'backupCount': 30,
            'formatter': 'audit',
            'level': 'INFO',
        },
        # Error logs
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG,
            'maxBytes': 10485760,
            'backupCount': 30,
            'formatter': 'error',
            'level': 'ERROR',
        },
        # Performance logs
        'perf_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PERFORMANCE_LOG,
            'maxBytes': 10485760,
            'backupCount': 30,
            'formatter': 'performance',
            'level': 'INFO',
        },
        # Database logs
        'db_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DB_LOG,
            'maxBytes': 10485760,
            'backupCount': 10,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        # Console
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        # Email
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'error',
            'level': 'ERROR',
        },
    },

    'loggers': {
        # Django core
        'django': {
            'handlers': ['console', 'app_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['db_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['perf_file', 'app_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Application logs
        'apps': {
            'handlers': ['console', 'app_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.authentication': {
            'handlers': ['console', 'app_file', 'security_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.common': {
            'handlers': ['console', 'app_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Security
        'security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Audit
        'audit': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Errors
        'errors': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Performance
        'performance': {
            'handlers': ['perf_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'root': {
        'handlers': ['console', 'app_file', 'error_file'],
        'level': 'WARNING',
    },
}