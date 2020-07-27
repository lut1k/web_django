import json
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from application.forms import UserSettingsForm, RegisterUserForm, AskForm, AnswerForm, LaskAuthenticationForm
from application.models import Question, Tag, Answer, LaskUser
from application.services import add_like, remove_like, get_type_object_from_str
from application.utilities import signer





class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(content=json.dumps(kwargs), content_type='application/json')


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(status='error', code=code, message=message)


# Check auth in Ajax
def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(code="no_auth", message=u'Authorization required')
        else:
            redirect(reverse('application:login'))
    return view2


class HomeListView(TemplateView):
    template_name = 'index.html'


class QuestionsListView(ListView):
    model = Question
    template_name = 'questions.html'
    context_object_name = 'questions'
    paginate_by = 20

    # Dictionary for selection queryset.
    filter_dict = {
        'all': Question.objects.all,
        'new': Question.objects.new_questions,
        'hot': Question.objects.hot_questions,
        'unanswered': Question.objects.unanswered_questions,
        'week': Question.objects.week_questions,
        'month': Question.objects.month_questions,
    }

    def dispatch(self, request, *args, **kwargs):
        self.tab = request.GET.get('tab', 'all')
        if self.tab not in self.filter_dict.keys():
            self.tab = 'all'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.filter_dict.get(self.tab)()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_number_of_questions'] = self.filter_dict.get(self.tab)().count()
        context['title'] = self.tab
        return context


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
            'user': self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'ask'
        return context


class AnswersToQuestionList(AccessMixin, MultipleObjectMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'question.html'
    paginate_by = 20
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
        return Answer.hot_answers.filter(question=self.target_question)

    def get_success_url(self):
        return reverse_lazy('application:answers-to-question', kwargs={'pk': self.target_question})

# ------------- Questions (change, delete, by tag) ---------------


class QuestionsChangeView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = AskForm
    template_name = 'ask.html'

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Your question has been successfully changed.')
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'question_id': self.kwargs.get('pk'),
        })
        return kwargs

    def get_success_url(self):
        return reverse_lazy("application:answers-to-question", kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'change'
        return context


class QuestionsDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('application:questions')

    def dispatch(self, request, *args, **kwargs):
        self.question_id = self.kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Your question deleted.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.question_id)


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

# ------------- Answers (change, delete) ---------------


class AnswerChangeView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm

    def dispatch(self, request, *args, **kwargs):
        self.target_answer = self.kwargs.get('pk')
        self.answer = get_object_or_404(Answer, id=self.target_answer)
        self.question = self.answer.question
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Your answer has been successfully changed.')
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'author': self.request.user,
            'question': self.question,
        })
        return kwargs

    def get_success_url(self):
        return reverse_lazy("application:answers-to-question", kwargs={'pk': self.question.id})


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Your answer deleted.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.answer = get_object_or_404(Answer, pk=self.kwargs.get('pk'))
        return self.answer

    def get_success_url(self):
        return reverse_lazy('application:answers-to-question', kwargs={'pk': self.answer.question.id})

# ------------- Tags ---------------


class TagsListView(ListView):
    model = Tag
    template_name = 'tags_list.html'
    context_object_name = 'tags'
    paginate_by = 36

    sorted_dict = {
        'popular': Tag.objects.get_tags_sorted_by_numbers_of_questions,
        'name': Tag.objects.get_tags_sorted_by_name,
        'new': Tag.objects.get_new_tags,
    }

    def dispatch(self, request, *args, **kwargs):
        self.filter_tags = request.GET.get('filter_tags')
        self.tab = request.GET.get('tab', 'new')
        if self.tab not in self.sorted_dict.keys():
            self.tab = 'new'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.filter_tags:
            return Tag.objects.filter(name__icontains=self.filter_tags)
        return self.sorted_dict.get(self.tab)()

# ------------- User, profile ---------------


class AskLoginView(LoginView):
    template_name = 'app_registration/login.html'
    authentication_form = LaskAuthenticationForm


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


@login_required_ajax
@require_POST
def like_object(request):
    user = request.user
    object_id = request.POST.get('id')
    action = request.POST.get('action')
    klass = get_type_object_from_str(request.POST.get('type'))
    obj = get_object_or_404(klass, id=object_id)
    if obj and action:
        if action == 'like':
            add_like(obj, user)
        elif action == 'unlike':
            remove_like(obj, user)
        like_count = obj.total_likes()
        return HttpResponseAjax(like_count=like_count, id_obj_like=obj.id)
    return HttpResponseAjaxError(code='outside error', message='server error')


@login_required_ajax
@require_POST
def correct_answer(request):
    user = request.user
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    if user != question.question_author:
        return HttpResponseBadRequest()
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    question.choose_correct_answer(answer)
    return HttpResponseAjax(correct_answer_id=answer.id)
