# book.py
class Book(BaseModel):
    title = models.CharField(max_length=500, db_index=True)
    author = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['available_quantity']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New book
            self.available_quantity = self.quantity
        super().save(*args, **kwargs)