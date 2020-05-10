from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from application.models import LaskUser
from .signals import user_registrated


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = LaskUser
        fields = ('email', 'nick_name', 'first_name', 'last_name', 'avatar', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email address')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html()
                                )
    password2 = forms.CharField(label='Password (second)',
                                widget=forms.PasswordInput,
                                help_text='Enter the same password again for verification'
                                )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != \
                self.cleaned_data['password2']:
            raise ValidationError("The password does not match ")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = LaskUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'avatar', 'send_messages')
