from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddressForm
from .models import User, Address, EmailOTP

def send_otp_email(user, otp_code):
    """Utility to dispatch styled 6-digit OTP verification email"""
    subject = "SPCart Account Verification OTP"
    context = {'user': user, 'otp_code': otp_code}
    
    html_content = render_to_string('accounts/otp_email.html', context)
    text_content = f"Hi {user.first_name or user.username},\n\nYour 6-digit SPCart Account Verification OTP is: {otp_code}\n\nValid for 10 minutes."

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Account inactive until OTP verified
            user.is_email_verified = False
            user.save()

            # Generate OTP & Send Email
            otp_obj = EmailOTP.generate_otp(user)
            send_otp_email(user, otp_obj.otp_code)

            request.session['verify_user_id'] = user.id
            messages.info(request, f'Verification OTP sent to {user.email}. Please enter the 6-digit code below.')
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        messages.warning(request, 'No pending account verification found. Please register first.')
        return redirect('accounts:register')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()

        latest_otp = EmailOTP.objects.filter(user=user).first()

        if latest_otp and latest_otp.otp_code == otp_input and latest_otp.is_valid():
            user.is_active = True
            user.is_email_verified = True
            user.save()

            # Clean up session & OTP
            latest_otp.delete()
            del request.session['verify_user_id']

            # Auto Login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'🎉 Account verified successfully! Welcome to SPCart, {user.first_name or user.username}.')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid or expired OTP code. Please enter the correct 6-digit code or click Resend.')

    return render(request, 'accounts/verify_otp.html', {'user': user})


def resend_otp_view(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        return redirect('accounts:register')

    user = get_object_or_404(User, id=user_id)
    otp_obj = EmailOTP.generate_otp(user)
    send_otp_email(user, otp_obj.otp_code)

    messages.success(request, f'A fresh 6-digit OTP code has been sent to {user.email}.')
    return redirect('accounts:verify_otp')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next') or 'core:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email/username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'addresses': addresses})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'user_form': user_form})


@login_required
def change_password_view(request):
    from django.contrib.auth.forms import PasswordChangeForm
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def addresses_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/addresses.html', {'addresses': addresses})


@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('accounts:addresses')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add New Address'})


@login_required
def edit_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('accounts:addresses')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required
def delete_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.info(request, 'Address deleted.')
    return redirect('accounts:addresses')
