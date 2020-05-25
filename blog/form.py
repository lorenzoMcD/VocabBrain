from .models import Test
from .models import Word
from .models import WordList
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class WordListForm(forms.ModelForm):
    class Meta:
        model = WordList
        fields = ['title', 'description']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description','wordlist']
