from abc import ABC, abstractmethod
from typing import Optional
from django.db import transaction
from tasks.models import JobTracker
from tasks.tasks import process_large_csv_task

class AsyncTask(ABC):
    """Abstract base class for async operations"""
    
    @abstractmethod
    def submit_task(self, *args, **kwargs) -> str:
        """Submit task and return job ID"""
        pass
    
    @abstractmethod
    def get_status(self, job_id: str) -> dict:
        """Get task status"""
        pass

class CSVProcessingService(AsyncTask):
    
    @transaction.atomic
    def submit_task(self, file_path: str, user_id: int) -> str:
        """Submit CSV processing task with job tracking"""
        
        # Create job tracker
        job = JobTracker.objects.create(
            job_type='CSV_UPLOAD',
            status='PENDING',
            initiated_by_id=user_id,
            metadata={'file_path': file_path}
        )
        
        # Submit to Celery via abstracted interface
        from tasks.tasks import csv_processor
        task = csv_processor.delay(file_path, job.id)
        
        # Update job with Celery task ID
        job.celery_task_id = task.id
        job.save()
        
        return job.id
    
    def get_status(self, job_id: str) -> dict:
        job = JobTracker.objects.get(id=job_id)
        
        # Get result from Celery if available
        if job.celery_task_id:
            from celery.result import AsyncResult
            result = AsyncResult(job.celery_task_id)
            
            return {
                'status': job.status,
                'celery_status': result.status,
                'progress': job.progress,
                'result': job.result,
                'errors': job.errors,
            }
        
        return {'status': job.status}