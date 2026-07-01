from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'total_quantity', 'available_quantity']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['publisher']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'borrow_date', 'due_date', 'status']
    list_filter = ['status']
    search_fields = ['student__username', 'book__title']
    date_hierarchy = 'borrow_date'