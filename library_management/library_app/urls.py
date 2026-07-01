from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Student URLs
    path('student/books/', views.student_books, name='student_books'),
    path('student/borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('student/return/<int:record_id>/', views.return_book, name='return_book'),
    path('student/history/', views.student_history, name='student_history'),

    # Admin URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/books/', views.admin_books, name='admin_books'),
    path('admin/book/add/', views.admin_book_add, name='admin_book_add'),
    path('admin/book/edit/<int:book_id>/', views.admin_book_edit, name='admin_book_edit'),
    path('admin/book/delete/<int:book_id>/', views.admin_book_delete, name='admin_book_delete'),
    path('admin/borrow_records/', views.admin_borrow_records, name='admin_borrow_records'),
    path('admin/statistics/', views.admin_statistics, name='admin_statistics'),
]