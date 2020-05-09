from django.urls import path
from application import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('hot/', views.HotQuestionsListView.as_view(), name='hot-questions'),
    path('tag/<int:pk>/', views.QuestionsByTagView.as_view(), name='questions-by-tag'),
    path('question/<int:pk>/', views.AnswersToQuestionList.as_view(), name='answers-to-question'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.AskTemplate.as_view(), name='ask'),
]
