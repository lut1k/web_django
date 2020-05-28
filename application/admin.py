import datetime
from django.contrib import admin
from application.models import Question, Tag, Like, Answer, LaskUser
from application.utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Email alert sent to users')


send_activation_notifications.short_description = 'Sending activation notification emails'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Passed activation?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Passed'),
            ('threedays', 'Activation failed for more than three days'),
            ('week', 'Activation failed for more than a week'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class LaskUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'avatar', 'email', 'is_activated', 'date_joined']
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter, )
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        ('groups', 'user_permissions'),
        ('last_login', 'date_joined'),
              )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications, )

    class Meta:
        model = LaskUser


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_author', 'created_at']
    ordering = ['rating']
    search_fields = ['title']

    class Meta:
        model = Question


admin.site.register(LaskUser, LaskUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)


