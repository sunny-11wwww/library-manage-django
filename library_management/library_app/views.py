from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Sum, F
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import Book, BorrowRecord


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_books')
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'?????{user.username}?')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('student_books')
        else:
            messages.error(request, '?????????')
    return render(request, 'library_app/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if password != confirm_password:
            messages.error(request, '??????????')
            return render(request, 'library_app/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '???????')
            return render(request, 'library_app/register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = name
        user.save()
        messages.success(request, '?????????')
        return redirect('login')
    return render(request, 'library_app/register.html')


# ??? Student Views ???

@login_required
def student_books(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    search_query = request.GET.get('search', '')
    books = Book.objects.all()
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'library_app/student_books.html', context)


@login_required
def borrow_book(request, book_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    book = get_object_or_404(Book, id=book_id)
    if not book.is_available():
        messages.error(request, '??????????')
        return redirect('student_books')

    # Check if student already has this book borrowed
    existing = BorrowRecord.objects.filter(
        student=request.user, book=book, status__in=['borrowed', 'overdue']
    ).exists()
    if existing:
        messages.error(request, '????????????')
        return redirect('student_books')

    BorrowRecord.objects.create(
        student=request.user,
        book=book,
        due_date=timezone.now() + timedelta(days=30)
    )
    book.available_quantity -= 1
    book.save()
    messages.success(request, f'?????{book.title}????30?????')
    return redirect('student_history')


@login_required
def return_book(request, record_id):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    record = get_object_or_404(BorrowRecord, id=record_id, student=request.user)
    if record.status == 'returned':
        messages.info(request, '??????')
        return redirect('student_history')

    record.status = 'returned'
    record.return_date = timezone.now()
    record.save()
    record.book.available_quantity += 1
    record.book.save()
    messages.success(request, f'?????{record.book.title}??')
    return redirect('student_history')


@login_required
def student_history(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    records = BorrowRecord.objects.filter(student=request.user).select_related('book')
    # Auto-update overdue status
    now = timezone.now()
    for record in records.filter(status='borrowed', due_date__lt=now):
        record.status = 'overdue'
        record.save()
    context = {
        'records': BorrowRecord.objects.filter(student=request.user).select_related('book'),
        'now': timezone.now(),
    }
    return render(request, 'library_app/student_history.html', context)


# ??? Admin Views ???

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)


@login_required
@admin_required
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_borrowed = BorrowRecord.objects.filter(status__in=['borrowed', 'overdue']).count()
    total_students = User.objects.filter(is_staff=False).count()
    overdue_count = BorrowRecord.objects.filter(status='overdue').count()
    recent_records = BorrowRecord.objects.select_related('student', 'book').order_by('-borrow_date')[:10]

    context = {
        'total_books': total_books,
        'total_borrowed': total_borrowed,
        'total_students': total_students,
        'overdue_count': overdue_count,
        'recent_records': recent_records,
    }
    return render(request, 'library_app/admin_dashboard.html', context)


@login_required
@admin_required
def admin_books(request):
    books = Book.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    return render(request, 'library_app/admin_books.html', {'books': books, 'search_query': search_query})


@login_required
@admin_required
def admin_book_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST.get('publisher', '')
        isbn = request.POST['isbn']
        total_quantity = int(request.POST['total_quantity'])
        publish_date = request.POST.get('publish_date', '') or None
        description = request.POST.get('description', '')

        if Book.objects.filter(isbn=isbn).exists():
            messages.error(request, '?ISBN????')
            return render(request, 'library_app/admin_book_form.html', {'action': '??'})

        Book.objects.create(
            title=title, author=author, publisher=publisher,
            isbn=isbn, total_quantity=total_quantity,
            available_quantity=total_quantity,
            publish_date=publish_date, description=description
        )
        messages.success(request, f'???{title}??????')
        return redirect('admin_books')
    return render(request, 'library_app/admin_book_form.html', {'action': '??'})


@login_required
@admin_required
def admin_book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.publisher = request.POST.get('publisher', '')
        isbn = request.POST['isbn']
        if isbn != book.isbn and Book.objects.filter(isbn=isbn).exists():
            messages.error(request, '?ISBN?????????')
            return render(request, 'library_app/admin_book_form.html', {'book': book, 'action': '??'})
        book.isbn = isbn
        total_quantity = int(request.POST['total_quantity'])
        diff = total_quantity - book.total_quantity
        book.total_quantity = total_quantity
        book.available_quantity = max(0, book.available_quantity + diff)
        book.publish_date = request.POST.get('publish_date', '') or None
        book.description = request.POST.get('description', '')
        book.save()
        messages.success(request, f'???{book.title}??????')
        return redirect('admin_books')
    return render(request, 'library_app/admin_book_form.html', {'book': book, 'action': '??'})


@login_required
@admin_required
def admin_book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if BorrowRecord.objects.filter(book=book, status__in=['borrowed', 'overdue']).exists():
        messages.error(request, '???????????????')
        return redirect('admin_books')
    book.delete()
    messages.success(request, '???????')
    return redirect('admin_books')


@login_required
@admin_required
def admin_borrow_records(request):
    records = BorrowRecord.objects.select_related('student', 'book').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        records = records.filter(status=status_filter)
    search = request.GET.get('search', '')
    if search:
        records = records.filter(
            Q(student__username__icontains=search) |
            Q(book__title__icontains=search)
        )
    return render(request, 'library_app/admin_borrow_records.html', {
        'records': records,
        'status_filter': status_filter,
        'search': search,
    })


@login_required
@admin_required
def admin_statistics(request):
    now = timezone.now()

    # Most borrowed books
    most_borrowed = BorrowRecord.objects.values(
        'book__id', 'book__title', 'book__author'
    ).annotate(
        borrow_count=Count('id')
    ).order_by('-borrow_count')[:10]

    # Monthly borrow trends
    monthly_borrows = BorrowRecord.objects.annotate(
        month=TruncMonth('borrow_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')[:12]

    # Overdue statistics
    overdue_books = BorrowRecord.objects.filter(status='overdue').select_related('student', 'book')

    # Category stats
    status_stats = BorrowRecord.objects.values('status').annotate(count=Count('id'))

    # Total stats
    total_borrows = BorrowRecord.objects.count()
    active_borrows = BorrowRecord.objects.filter(status__in=['borrowed', 'overdue']).count()
    returned_borrows = BorrowRecord.objects.filter(status='returned').count()
    overdue_count = BorrowRecord.objects.filter(status='overdue').count()

    context = {
        'most_borrowed': most_borrowed,
        'monthly_borrows': monthly_borrows,
        'overdue_books': overdue_books,
        'status_stats': status_stats,
        'total_borrows': total_borrows,
        'active_borrows': active_borrows,
        'returned_borrows': returned_borrows,
        'overdue_count': overdue_count,
    }
    return render(request, 'library_app/admin_statistics.html', context)