from django import forms
from application.models import LaskUser


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = LaskUser
        fields = ('email', 'nick_name', 'first_name', 'last_name', 'avatar')


