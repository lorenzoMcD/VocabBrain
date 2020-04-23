from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    CHOICES = [('Student', 'Student'), ('Teacher', 'Teacher')
               ]
    selection = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2', 'selection']
