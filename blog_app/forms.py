from django import forms
from django.contrib.auth.models import *
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Artykul
        fields = ['nazwa', 'obraz', 'tresc']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Komentarz
        fields = ['tresc']
