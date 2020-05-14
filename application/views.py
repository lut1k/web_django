from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from application.forms import UserSettingsForm, RegisterUserForm, AskForm, AnswerForm
from application.models import Question, Tag, Answer, LaskUser
from application.utilities import signer


class HomeListView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 20
    queryset = Question.new_questions.all()


def other_page(request, page):
    try:
        template = get_template(page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class AskTemplate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = AskForm
    template_name = 'ask.html'
    success_url = '/question/{id}/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class HotQuestionsListView(ListView):
    model = Question
    template_name = 'hot.html'
    context_object_name = 'questions'
    paginate_by = 10
    queryset = Question.hot_questions.all()


class AnswersToQuestionList(AccessMixin, MultipleObjectMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'question.html'
    paginate_by = 30
    context_object_name = 'answers'

    def dispatch(self, request, *args, **kwargs):
        self.target_question = self.kwargs.get('pk')
        self.object_list = self.get_queryset()
        self.question = get_object_or_404(Question, id=self.target_question)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
            'question': self.question,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context

    def get_queryset(self):
        return Answer.objects.filter(question=self.target_question).order_by('-rating', 'created_at')

    def get_success_url(self):
        return reverse_lazy('application:answers-to-question', kwargs=({'pk': self.target_question}))


class QuestionsByTagView(ListView):
    model = Question
    template_name = 'questions_by_tag.html'
    paginate_by = 20
    context_object_name = 'questions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, id=self.kwargs.get("pk"))
        return context

    def get_queryset(self):
        return Question.objects.filter(tags=self.kwargs.get("pk")).order_by('-rating')


class AskLoginView(LoginView):
    template_name = 'app_registration/login.html'


class AskLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'app_registration/logged_out.html'


class UserProfile(TemplateView):
    template_name = 'app_registration/profile.html'


class UserSettings(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LaskUser
    form_class = UserSettingsForm
    success_url = reverse_lazy("application:settings")
    success_message = "User personal data has changed"
    template_name = 'app_registration/settings.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class AskPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'app_registration/password_change.html'
    success_url = reverse_lazy("application:profile")
    success_message = "User password changed"


class RegisterUserView(CreateView):
    model = LaskUser
    template_name = 'app_registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('application:register-done')


class RegisterDoneView(TemplateView):
    template_name = 'app_registration/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'app_registration/bad_signature.html')
    user = get_object_or_404(LaskUser, username=username)
    if user.is_activated:
        template = 'app_registration/user_is_activated.html'
    else:
        template = 'app_registration/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = LaskUser
    template_name = 'app_registration/delete_user.html'
    success_url = reverse_lazy('application:home')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
