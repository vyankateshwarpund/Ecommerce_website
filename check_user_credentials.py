import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from accounts.models import User

print("==================================================================")
print("CHECKING DATABASE USERS & CREDENTIALS")
print("==================================================================")

users = User.objects.all()
for u in users:
    print(f"ID: {u.id} | Email: '{u.email}' | Username: '{u.username}' | Active: {u.is_active} | Staff: {u.is_staff}")

print("==================================================================")
