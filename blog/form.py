from .models import Folder
from .models import Suggestion
from .models import Test
from .models import Testtaker
from .models import Word
from .models import WordList
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class WordListForm(forms.ModelForm):
    class Meta:
        model = WordList
        fields = ['title', 'description', 'worksheet_text', 'folder']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'wordlist', 'folder']


class FolderCreateForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['title', 'description']


class TestSubmitForm(forms.ModelForm):
    class Meta:
        model = Testtaker
        fields = ['tester', 'test', 'score']


class SuggestionForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Suggestion
        fields = ['name', 'email', 'comment']
