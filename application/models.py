from django.contrib.auth.models import User, AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class LaskUser(AbstractUser):
    nick_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)
    rating = models.IntegerField(default=0)
    send_messages = models.BooleanField(default=True, verbose_name="Send you a notification?")
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Passed activation?')

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
        return '{}...; user: {}; updated_at: {}'.format(self.title[:15], self.question_author, self.updated_at)


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_author = models.ForeignKey(LaskUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()

    def __str__(self):
        return "{}, updated_at: {}; text: {}".format(self.answer_author, self.updated_at, self.text[:20])


class Like(models.Model):
    pass
