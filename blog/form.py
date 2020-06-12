from .models import Test
from .models import Testtaker
from .models import Word
from .models import WordList
from .models import Suggestion
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class WordListForm(forms.ModelForm):
    class Meta:
        model = WordList
        fields = ['title', 'description', 'worksheet_text']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'wordlist']


class TestSubmitForm(forms.ModelForm):
    class Meta:
        model = Testtaker
        fields = ['tester', 'test', 'score']


class SuggestionForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Suggestion
        fields = ['name', 'email', 'comment']
