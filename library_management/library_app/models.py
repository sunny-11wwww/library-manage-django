from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    title = models.CharField("??", max_length=200)
    author = models.CharField("??", max_length=100)
    publisher = models.CharField("???", max_length=200, blank=True)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    total_quantity = models.IntegerField("???", default=1)
    available_quantity = models.IntegerField("????", default=1)
    publish_date = models.DateField("????", null=True, blank=True)
    description = models.TextField("??", blank=True)
    created_at = models.DateTimeField("????", auto_now_add=True)
    updated_at = models.DateTimeField("????", auto_now=True)

    class Meta:
        verbose_name = "??"
        verbose_name_plural = "??"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_quantity > 0


class BorrowRecord(models.Model):
    STATUS_CHOICES = (
        ('borrowed', '???'),
        ('returned', '???'),
        ('overdue', '??'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="??", limit_choices_to={'is_staff': False})
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="??")
    borrow_date = models.DateTimeField("????", auto_now_add=True)
    due_date = models.DateTimeField("????")
    return_date = models.DateTimeField("????", null=True, blank=True)
    status = models.CharField("??", max_length=20, choices=STATUS_CHOICES, default='borrowed')

    class Meta:
        verbose_name = "????"
        verbose_name_plural = "????"
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.student.username} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def days_overdue(self):
        if self.status == 'returned':
            return 0
        overdue = timezone.now() - self.due_date
        return max(0, overdue.days)