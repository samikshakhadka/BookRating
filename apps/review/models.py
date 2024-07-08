# review/models.py
from django.db import models
from django.conf import settings
from apps.book.models import Book
from apps.user.models import CustomUser 
from django.core.validators import MaxValueValidator, MinValueValidator

class Opinion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.email}'
