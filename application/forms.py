from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import FileInput
from application.models import LaskUser, Question, Tag, Answer
from .signals import user_registrated


class LaskAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={'placeholder': "Login"})
                               )
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': "Password"}),
                               help_text=password_validation.password_validators_help_text_html()
                               )


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    avatar = forms.ImageField(label='Avatar', required=False, widget=FileInput)

    class Meta:
        model = LaskUser
        fields = ('email', 'nick_name', 'first_name', 'last_name', 'avatar', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email address')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html()
                                )
    password2 = forms.CharField(label='Password (again)',
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


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=50,
                           label='Question tags',
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a tags ...'}),
                           help_text='You can add up to three tags to the question. Enter a comma ","')

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Enter a title ..."}),
            'text': forms.Textarea(attrs={'placeholder': "Enter a question ..."}),
        }
        labels = {'text': 'Question text'}

    def __init__(self, user, question_id=None, *args, **kwargs):
        self._user = user
        self.question_id = question_id
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        tags = [tag.strip() for tag in self.cleaned_data['tags'].split(',')]
        if len(tags) > 3:
            raise forms.ValidationError(u'Maximum 3 tags.', code='tags_count')
        return tags

    def save(self, commit=True):
        tag_names = self.cleaned_data['tags']
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        question, created = Question.objects.update_or_create(id=self.question_id,
                                                              defaults={'title': self.cleaned_data['title'],
                                                                        'text': self.cleaned_data['text'],
                                                                        'question_author': self._user,
                                                                        })
        question.tags.set(tags)
        return question


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Enter your answer..."}), label='')

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, author, question, *args, **kwargs):
        self.author = author
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.answer_author = self.author
        answer.question = self.question
        if commit:
            answer.save()
        return answer


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='',
                              widget=forms.Textarea(attrs={'placeholder': "Search..."}))
