"""
Custom exception handler for REST API.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the error response
        error_data = {
            'status': 'error',
            'message': response.data.get('detail', 'An error occurred'),
            'code': response.status_code,
            'errors': response.data
        }
        response.data = error_data
    else:
        # Handle uncaught exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        error_data = {
            'status': 'error',
            'message': 'An internal server error occurred',
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'errors': {}
        }
        response = Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response