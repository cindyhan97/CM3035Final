from django import forms
from django.db.models import fields
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('nickname','photo')

class userlogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
class postForm(forms.ModelForm):
    class Meta:
        model = userPost
        fields = ('text','mediaFile1','mediaFile2', 'mediaFile3')
class publicChatForm(forms.ModelForm):
    class Meta:
        model = publicChat
        fields = ('comment',)
