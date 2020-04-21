from django.contrib import admin

from application.models import Profile, Question, Tag, Like, Answer

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)
