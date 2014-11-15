from main.models import *
from django.contrib.auth.models import User
from django import forms

#using http://www.tangowithdjango.com/book/chapters/login.html
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','password')
