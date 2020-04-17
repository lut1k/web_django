from django.urls import path

from application import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hot/', views.hot_questions, name='hot-questions'),
    path('tag/blablabla/', views.questions_by_tag, name='questions-by-tag'),
    path('question/35/', views.answers_to_question, name='answers-to-question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
]
