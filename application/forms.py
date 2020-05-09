from django import forms
from django.contrib.auth.models import User
from application.models import LaskUser


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = LaskUser
        fields = ('username', 'email', 'nick_name', 'first_name', 'last_name', 'avatar')


