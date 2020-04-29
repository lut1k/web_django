import re
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from application.models import Question, Tag, Answer


class HomeLisView(ListView):
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
        context['question'] = Question.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        return Answer.objects.filter(question=self.kwargs.get('pk')).order_by('-rating', '-created_at')


class QuestionsByTagView(ListView):
    model = Question
    template_name = 'questions_by_tag.html'
    paginate_by = 20
    context_object_name = 'questions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(id=self.kwargs.get("pk"))
        return context

    def get_queryset(self):
        return Question.objects.filter(tags=self.kwargs.get("pk")).order_by('-rating')


@login_required
def settings(request):
    return render(request, 'settings.html')


class AskTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'ask.html'


def signup(request):
    return render(request, 'signup.html')
