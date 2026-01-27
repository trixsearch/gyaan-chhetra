# student.py
class Student(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50, unique=True, db_index=True)
    student_class = models.ForeignKey('Class', on_delete=models.PROTECT)
    allowed_to_use_library = models.BooleanField(default=True)
    status = models.CharField(
        max_length=3,
        choices=[('APP', 'Approved'), ('PEN', 'Pending'), ('TER', 'Terminated')],
        default='PEN'
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['roll_number', 'student_class'],
                name='unique_roll_per_class'
            )
        ]
        indexes = [
            models.Index(fields=['status', 'allowed_to_use_library']),
        ]   