from django.shortcuts import render
from django.views.generic import ListView
from application.models import Question


class HomeLisView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 2
    queryset = Question.new_questions.all()


class HotQuestionsListView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 2
    queryset = Question.hot_questions.all()


def questions_by_tag(request):
    return render(request, 'index.html')


def answers_to_question(request):
    return render(request, 'question.html')


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
