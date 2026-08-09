from django import forms
from django.contrib.auth import get_user_model
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
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
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
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username_or_email and password:
            # 1. Check if username_or_email matches an email address
            user_obj = User.objects.filter(email__iexact=username_or_email).first()
            if not user_obj:
                # 2. Check if it matches a username
                user_obj = User.objects.filter(username__iexact=username_or_email).first()

            if user_obj:
                from django.contrib.auth import authenticate
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    if not user.is_active:
                        raise forms.ValidationError("This account is inactive.")
                    self.user_cache = user
                    return cleaned_data

            raise forms.ValidationError("Please enter a correct email/username and password. Note that passwords are case-sensitive.")
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'profile_image', 'gender', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line', 'area', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_line': forms.Textarea(attrs={'rows': 3, 'placeholder': 'House no, building, street...'}),
        }
