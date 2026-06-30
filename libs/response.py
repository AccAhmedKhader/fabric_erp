"""
Standardized API response utilities.
"""

from django.http import JsonResponse


def success_response(data=None, message='Success', status=200):
    """
    Return a success response.
    """
    return JsonResponse({
        'status': 'success',
        'message': message,
        'data': data
    }, status=status)


def error_response(message='Error', errors=None, status=400):
    """
    Return an error response.
    """
    return JsonResponse({
        'status': 'error',
        'message': message,
        'errors': errors
    }, status=status)


def api_response(data=None, message='OK', success=True, status=200):
    """
    Return a generic API response.
    """
    return JsonResponse({
        'success': success,
        'message': message,
        'data': data
    }, status=status)