import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from accounts.models import User

users = User.objects.filter(email__in=['admin@spcart.com', 'pundsaurav@gmail.com'])
for u in users:
    u.is_staff = True
    u.save()
    print(f"Granted staff access to {u.email} (is_staff={u.is_staff})")
