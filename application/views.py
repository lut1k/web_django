from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView
from application.forms import UserSettingsForm
from application.models import Question, Tag, Answer, LaskUser


class HomeListView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 20
    queryset = Question.new_questions.all()


class HotQuestionsListView(ListView):
    model = Question
    template_name = 'hot.html'
    context_object_name = 'questions'
    paginate_by = 10
    queryset = Question.hot_questions.all()


class AnswersToQuestionList(ListView):
    model = Answer
    template_name = 'question.html'
    paginate_by = 30
    context_object_name = 'answers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        target_question = self.kwargs.get('pk')
        return Answer.objects.filter(question=target_question).order_by('-rating', '-created_at')


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


class UserProfile(TemplateView):
    template_name = 'registration/profile.html'


class UserSettings(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LaskUser
    form_class = UserSettingsForm
    success_url = reverse_lazy("settings")
    success_message = "User’s personal data has changed"
    template_name = 'registration/settings.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class AskTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'ask.html'


def signup(request):
    return render(request, 'registration/signup.html')
