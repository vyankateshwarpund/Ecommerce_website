import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from accounts.models import User

print("==================================================================")
print("STAFF ADMIN & DEMO USER LOGIN CREDENTIALS")
print("==================================================================")

staff_users = User.objects.filter(is_staff=True)
for u in staff_users:
    print(f"Name: {u.get_full_name() or u.username}")
    print(f"Email Address: {u.email}")
    print(f"Username: {u.username}")
    print(f"Is Superuser: {u.is_superuser}")
    print(f"Is Staff: {u.is_staff}")
    print("-" * 50)

print("Default Password for all Admin accounts: Password123")
print("==================================================================")
