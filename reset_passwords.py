import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from accounts.models import User

# Set known password for users
default_pass = "Password123"

for u in User.objects.all():
    u.set_password(default_pass)
    u.save()
    print(f"Updated password for {u.email} ({u.username}) to '{default_pass}'")

print("All user passwords reset successfully to 'Password123'!")
