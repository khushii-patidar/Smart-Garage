import os
import django
import sys

sys.path.append(r"c:\Users\Ambika\Downloads\smartgarage-phase1\smartgarage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User

users = User.objects.all()
for u in users:
    print(f"User: {u.username}, Role: {u.role}, is_superuser: {u.is_superuser}")
