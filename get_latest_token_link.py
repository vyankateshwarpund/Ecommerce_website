import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.models import User

user = User.objects.get(email='pundsaurav@gmail.com')
uid = urlsafe_base64_encode(force_bytes(user.pk))
token = default_token_generator.make_token(user)

fresh_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"
print("==================================================================")
print("FRESH VALID PASSWORD RESET LINK:")
print(fresh_link)
print("==================================================================")
