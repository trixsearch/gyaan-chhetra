from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import DatabaseError
from celery.exceptions import TimeoutError
import logging

logger = logging.getLogger(__name__)

class BusinessLogicError(Exception):
    """Custom exception for business logic failures"""
    pass

def custom_exception_handler(exc, context):
    """Global exception handler with structured responses"""
    
    # Call REST framework's default handler first
    response = exception_handler(exc, context)
    
    if response is None:
        # Handle uncaught exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        if isinstance(exc, DatabaseError):
            response_data = {
                'error': 'database_error',
                'message': 'A database error occurred',
                'reference_id': generate_reference_id(),
            }
            response = Response(response_data, status=503)
        
        elif isinstance(exc, BusinessLogicError):
            response_data = {
                'error': 'business_logic_error',
                'message': str(exc),
                'reference_id': generate_reference_id(),
            }
            response = Response(response_data, status=400)
        
        else:
            # Generic error
            response_data = {
                'error': 'internal_server_error',
                'message': 'An unexpected error occurred',
                'reference_id': generate_reference_id(),
            }
            response = Response(response_data, status=500)
    
    return response

# Retry decorator for Celery tasks
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_csv_with_retry(self, file_path, job_id):
    try:
        # Process CSV
        result = process_csv_file(file_path)
        return result
        
    except TimeoutError as exc:
        try:
            # Exponential backoff
            self.retry(exc=exc, countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            # Update job as failed
            update_job_status(job_id, 'FAILED', str(exc))
            raise