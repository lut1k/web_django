from django.urls import path
from application import views
from .views import UserSettings, UserProfile, AskPasswordChangeView, RegisterUserView, RegisterDoneView, \
    user_activate, AskLoginView, AskLogoutView, DeleteUserView, other_page

app_name = 'application'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('questions', views.QuestionsListView.as_view(), name='questions'),
    path('tag/<int:pk>/', views.QuestionsByTagView.as_view(), name='questions-by-tag'),
    path('question/<int:pk>/', views.AnswersToQuestionList.as_view(), name='answers-to-question'),
    path('ask/', views.AskTemplate.as_view(), name='ask'),
    path('like/', views.like_object, name='like'),
    path('correct_answer/', views.correct_answer, name='correct-answer'),
    path('<str:page>/', other_page, name='other'),
]

# Add Django site authentication urls (for login, register, profile, settings)
urlpatterns += [
    path('accounts/login/', AskLoginView.as_view(), name='login'),
    path('accounts/logout/', AskLogoutView.as_view(), name='logout'),
    path('accounts/profile/', UserProfile.as_view(), name='profile'),
    path('accounts/profile/edit/', UserSettings.as_view(), name='settings'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile-delete'),
    path('accounts/password/change/', AskPasswordChangeView.as_view(), name='password-change'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register-done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register-activate'),
]
