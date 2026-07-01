from django.shortcuts import redirect
from django.urls import reverse

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path.startswith('/admin_dashboard') or request.path.startswith('/admin/'):
                if not request.user.is_staff:
                    return redirect('home')
        response = self.get_response(request)
        return response