# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'autocomplete': 'username',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'autocomplete': 'current-password',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
    }))

class ProfileCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    class Meta:
        model = User
        fields = ['email', 'password']

# Add to forms.py
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'phone_number']
        widgets = {
            'address_line1': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
        }