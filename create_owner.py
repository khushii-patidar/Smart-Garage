import os
import django
import sys

sys.path.append(r"c:\Users\Ambika\Downloads\smartgarage-phase1\smartgarage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User

# Check if boss exists
if not User.objects.filter(username='boss').exists():
    user = User.objects.create_user(username='boss', password='BossPassword123!', email='boss@garage.com')
    user.role = User.Role.OWNER
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Owner created! Username: boss, Password: BossPassword123!")
else:
    print("Owner already exists!")
