from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count
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
        return super().get_queryset().annotate(count=Count('rating')).order_by('-count', '-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    question_author = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = GenericRelation('Like')
    tags = models.ManyToManyField(Tag, blank=True)
    correct_answer = models.OneToOneField('Answer', related_name='+', null=True, blank=True, on_delete=models.CASCADE)

    objects = models.Manager()
    new_questions = NewQuestionsManager()
    hot_questions = HotQuestionsManager()

    def __str__(self):
        return '{}...; user: {};'.format(self.title[:15], self.question_author)

    def total_likes(self):
        return self.rating.count()

    def get_users_id_who_liked_question(self):
        return self.rating.all().values_list('user_id', flat=True)

    def get_class(self):
        return self.__class__

    def choose_correct_answer(self, answer):
        if answer in self.answers.all():
            self.correct_answer = answer
            self.save()


class HotAnswersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(count=Count('rating')).order_by('-count', '-created_at')


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_author = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = GenericRelation('Like')

    objects = models.Manager()
    hot_answers = HotAnswersManager()

    def __str__(self):
        return "{}; text: {}".format(self.answer_author, self.text[:50])

    def total_likes(self):
        return self.rating.count()

    def get_users_id_who_liked_question(self):
        return self.rating.all().values_list('user_id', flat=True)

    def get_class(self):
        return self.__class__


class Like(models.Model):
    user = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default='')
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Like. user - {}. object - {}".format(self.user, self.content_object)
