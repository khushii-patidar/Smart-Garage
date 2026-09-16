import os
import django
import sys

sys.path.append(r"c:\Users\Ambika\Downloads\smartgarage-phase1\smartgarage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.forms import CustomerSignUpForm

form = CustomerSignUpForm({
    'username': 'khushi',
    'first_name': 'Khushbu',
    'last_name': 'Patidar',
    'email': 'khushbu@gmail.com',
    'phone': '9264337475',
    'password1': 'Khushi@123',
    'password2': 'Khushi@123',
})

print("Is valid?", form.is_valid())
if not form.is_valid():
    print("Errors:", form.errors)
