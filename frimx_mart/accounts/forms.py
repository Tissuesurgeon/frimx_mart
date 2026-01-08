from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    location = forms.CharField(required=False)
    profile_image = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 
                 'location', 'profile_image']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'location', 'profile_image']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'website', 'facebook', 'instagram', 'twitter', 'preferred_contact']