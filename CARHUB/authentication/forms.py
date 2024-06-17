from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

USER_TYPE_CHOICES = (
    ('dealer', 'Dealer'),
    ('customer', 'Customer'),
)

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True, label="Register as")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
