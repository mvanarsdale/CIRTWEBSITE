from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Or your custom user model

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')  # Add role to fields