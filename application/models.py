from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path)
    rating = models.IntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    # TODO почитать что такое 'Answer'
    correct_answer = models.OneToOneField('Answer', related_name='+', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}; user: {}; updated_at: {}'.format(self.title, self.question_author, self.updated_at)


class Answer(models.Model):
    text = models.TextField()
    answer_author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirm_flag = models.BooleanField()
    rating = models.IntegerField()

    def __str__(self):
        return "{}, updated_at: {}; text: {}".format(self.answer_author, self.updated_at, self.text)


class Like(models.Model):
    pass
