from django.contrib.auth.models import AbstractUser
from django.db import models
from application.utilities import get_user_directory_path


class LaskUser(AbstractUser):
    nick_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to=get_user_directory_path, blank=True)
    rating = models.IntegerField(default=0)
    send_messages = models.BooleanField(default=True, verbose_name="Send you a notification?")
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Passed activation?')

    def get_avatar(self):
        if not self.avatar:
            return '/static/images/avatar_default.jpg'
        return self.avatar.url

    class Meta(AbstractUser.Meta):
        pass


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.name


class NewQuestionsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')


class HotQuestionsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-rating', '-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    question_author = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    correct_answer = models.OneToOneField('Answer', related_name='+', null=True, blank=True, on_delete=models.CASCADE)

    objects = models.Manager()
    new_questions = NewQuestionsManager()
    hot_questions = HotQuestionsManager()

    def __str__(self):
        return '{}...; user: {};'.format(self.title[:15], self.question_author)


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_author = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return "{}; text: {}".format(self.answer_author, self.text[:50])


class Like(models.Model):
    pass
