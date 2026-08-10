from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Address

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Minimum 8 characters', 'class': 'form-control'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email_clean = email.strip()
            existing_user = User.objects.filter(email__iexact=email_clean).first()
            if existing_user:
                if existing_user.is_email_verified or existing_user.is_active:
                    raise forms.ValidationError("An account with this email address already exists. Please login instead.")
                else:
                    # Clean up stale unverified inactive account so user can re-register and receive fresh OTP
                    existing_user.delete()
            return email_clean
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        # Auto-generate unique username from email prefix
        base_username = user.email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Email Address or Username", widget=forms.TextInput(attrs={
        'placeholder': 'Enter email address or username',
        'class': 'form-control',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control'
    }))

    def clean(self):
        cleaned_data = super().clean()
        raw_input = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if raw_input and password:
            query = raw_input.strip()
            password = password.strip()

            # 1. Search DB for matching email OR username (case-insensitive)
            user_obj = User.objects.filter(
                Q(email__iexact=query) | Q(username__iexact=query)
            ).first()

            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    if not user.is_active:
                        raise forms.ValidationError("This account is inactive or email is not verified.")
                    self.user_cache = user
                    return cleaned_data

            # 2. Direct authenticate fallback
            user = authenticate(username=query, password=password)
            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError("This account is inactive or email is not verified.")
                self.user_cache = user
                return cleaned_data

            raise forms.ValidationError("Please enter a correct email/username and password. Note that passwords are case-sensitive.")

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line', 'area', 'city', 'state', 'postal_code', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile Number'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flat / House No. / Building / Street'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality / Area / Landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-digit Pincode'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
