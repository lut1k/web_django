import re
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from application.models import Question


class HomeLisView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 20
    queryset = Question.new_questions.all()


class HotQuestionsListView(ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 20
    queryset = Question.hot_questions.all()


class QuestionDetail(DetailView):
    model = Question
    template_name = 'question.html'
    paginate_by = 20


def questions_by_tag(request):
    return render(request, 'index.html')





def settings(request):
    return render(request, 'settings.html')


class AskTemplate(TemplateView):
    template_name = 'ask.html'


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def get_continue(request, default='/'):
    url = request.GET.get('continue', default)
    if re.match(r'^/|http://127\.0\.0\.', url):   # Защита от Open Redirect
        return url
    return default


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(get_continue(request))
