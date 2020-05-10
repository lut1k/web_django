from django.contrib import admin
from application.models import Question, Tag, Like, Answer, LaskUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'avatar', 'email', 'first_name', 'last_name', 'rating', 'send_messages', 'is_activated']
    ordering = ['username']
    search_fields = ['username']

    class Meta:
        model = LaskUser


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_author', 'rating', 'created_at']
    ordering = ['rating']

    class Meta:
        model = Question


admin.site.register(LaskUser, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)


