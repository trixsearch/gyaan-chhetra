# borrow.py
class BorrowRecord(BaseModel):
    """Optimized for frequent queries"""
    book = models.ForeignKey(Book, on_delete=models.PROTECT, db_index=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, db_index=True)
    borrowed_date = models.DateField(auto_now_add=True, db_index=True)
    due_date = models.DateField(db_index=True)
    returned_date = models.DateField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)
    penalty_applied = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['student', 'returned_date']),
            models.Index(fields=['due_date', 'is_overdue']),
            models.Index(fields=['book', 'returned_date']),
        ]