from django.urls import path

from application import views

urlpatterns = [
    path('', views.HomeLisView.as_view(), name='home'),
    path('hot/', views.HotQuestionsListView.as_view(), name='hot-questions'),
    path('tag/blablabla/', views.questions_by_tag, name='questions-by-tag'),
    path('question/35/', views.answers_to_question, name='answers-to-question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('ask/', views.AskTemplate.as_view(), name='ask'),
    path('settings/', views.settings, name='settings')
]
