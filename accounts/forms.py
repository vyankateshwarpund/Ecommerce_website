from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Address

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username (optional)'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'form-control',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control'
    }))


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
