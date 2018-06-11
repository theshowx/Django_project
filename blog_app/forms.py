from django import forms
from .models import *

class UserForm(forms.ModelForm):
    hasło = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'hasło']

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Artykul
        fields = ['nazwa', 'obraz', 'tresc']

class PrivateArticleForm(forms.ModelForm):
    hasło = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Artykul
        fields = ['nazwa', 'obraz', 'tresc', 'hasło']

class AccessArticleForm(forms.Form):
    hasło = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['hasło']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Komentarz
        fields = ['tresc']
