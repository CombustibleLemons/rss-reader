from main.models import *
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'password')
