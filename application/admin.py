from django.contrib import admin
from application.models import Profile, Question, Tag, Like, Answer


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']
    ordering = ['user']
    search_fields = ['user_id']

    class Meta:
        model = Profile


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_author']

    class Meta:
        model = Question


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)


