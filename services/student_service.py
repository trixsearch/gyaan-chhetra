from django.db import transaction, DatabaseError
from django.db.models import Q, Count
from apps.users.models import Student
from common.utils.exceptions import BusinessLogicError

class StudentService:
    
    @staticmethod
    @transaction.atomic
    def create_student(user_data, student_data, created_by):
        """Atomic student creation with audit"""
        try:
            # Create user first
            from apps.users.services import UserService
            user = UserService.create_user(user_data, created_by)
            
            # Create student profile
            student = Student.objects.create(
                user=user,
                created_by=created_by,
                **student_data
            )
            
            # Log audit trail
            AuditLogService.log_create(
                user=created_by,
                model='Student',
                instance_id=student.id
            )
            
            return student
            
        except DatabaseError as e:
            # Automatic rollback on exception
            raise BusinessLogicError(f"Failed to create student: {str(e)}")
    
    @staticmethod
    def get_students_with_optimized_queries(filters=None):
        """Optimized query with select_related and prefetch_related"""
        queryset = Student.objects.filter(is_deleted=False)\
            .select_related(
                'user',
                'student_class',
                'created_by__userprofile'  # If exists
            )\
            .prefetch_related(
                'borrowrecord_set',
                'borrowrecord_set__book'
            )
        
        if filters:
            queryset = queryset.filter(**filters)
        
        # Use iterator() for large datasets
        return queryset
    
    @staticmethod
    def disable_student(student_id, disabled_by):
        """Soft delete with validation"""
        student = Student.objects.get(id=student_id, is_deleted=False)
        
        # Check if student has pending books
        pending_books = student.borrowrecord_set.filter(
            returned_date__isnull=True
        ).exists()
        
        if pending_books:
            raise BusinessLogicError(
                "Cannot disable student with pending books"
            )
        
        student.allowed_to_use_library = False
        student.updated_by = disabled_by
        student.save()
        
        return student