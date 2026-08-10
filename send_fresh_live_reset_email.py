import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.contrib.auth.forms import PasswordResetForm

print("==================================================================")
print("DISPATCHING FRESH HTML GMAIL PASSWORD RESET EMAIL")
print("==================================================================")

form = PasswordResetForm({'email': 'pundsaurav@gmail.com'})
if form.is_valid():
    form.save(
        email_template_name='accounts/password_reset_email.txt',
        html_email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        use_https=False,
        domain_override='127.0.0.1:8000',
        from_email='SPCart Support <pundsaurav@gmail.com>'
    )
    print("SUCCESS: Beautiful HTML Gmail SMTP password reset email sent to pundsaurav@gmail.com!")
else:
    print(f"Form errors: {form.errors}")

print("==================================================================")
