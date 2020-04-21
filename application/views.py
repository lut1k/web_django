from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def hot_questions(request):
    return render(request, 'index.html')


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
