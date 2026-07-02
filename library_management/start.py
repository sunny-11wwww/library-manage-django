"""
Railway production startup script.
Runs migrations, creates admin user, collects static files, then starts Gunicorn.
"""
import os
import sys
import subprocess

# Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management.settings")

# ── Step 1: Run database migrations ──
print("[start.py] Running database migrations...")
subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
print("[start.py] Migrations complete.")

# ── Step 2: Collect static files ──
print("[start.py] Collecting static files...")
subprocess.run(
    [sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"],
    check=True,
)
print("[start.py] Static files collected.")

# ── Step 3: Ensure admin user exists ──
print("[start.py] Ensuring admin user exists...")
import django

django.setup()
from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("[start.py] Admin user created: admin / admin123")
else:
    print("[start.py] Admin user already exists.")

# ── Step 4: Start Gunicorn ──
port = os.environ.get("PORT", "8000")
print(f"[start.py] Starting Gunicorn on 0.0.0.0:{port} ...")
os.execvp(
    "gunicorn",
    [
        "gunicorn",
        "library_management.wsgi:application",
        "--bind",
        f"0.0.0.0:{port}",
        "--workers",
        "4",
        "--access-logfile",
        "-",
    ],
)