import time
import random
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from application.models import Question, Tag, Answer, LaskUser

USERS_COUNT = 500
QUESTIONS_COUNT = 500
ANSWERS_COUNT = 30000
TAGS_COUNT = 2000
VOTES_COUNT = 1000


# TODO дописать заполнение лайков после реализации логики лайков
# python manage.py testdata
class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **options):
        TestDataForDb.create_users()
        TestDataForDb.create_tags()
        TestDataForDb.create_questions()
        TestDataForDb.create_answers()


stdout_writer = Command()


class TestDataForDb:
    @classmethod
    def create_users(cls):
        users = []
        faker = Faker()
        for i in range(USERS_COUNT):
            users.append(LaskUser(username=faker.user_name() + str(i),
                                  email=faker.email(),
                                  password=make_password('admin'),
                                  nick_name=faker.word()
                                  )
                         )
        LaskUser.objects.bulk_create(users, USERS_COUNT)
        stdout_writer.stdout.write("Created test data: USERS")

    @classmethod
    def create_tags(cls):
        faker = Faker()
        for i in range(TAGS_COUNT):
            tag = Tag(name=faker.word())
            try:
                tag.save()
            except IntegrityError:
                continue
        stdout_writer.stdout.write("Created test data: TAGS")

    @classmethod
    def create_questions(cls):
        users = LaskUser.objects.all()
        tags = Tag.objects.all()
        faker = Faker()
        for _ in range(QUESTIONS_COUNT):
            question = Question(title=faker.sentence(),
                                text=faker.text(),
                                question_author=random.choice(users),
                                rating=random.randint(1, 100),
                                )
            question.save()
            for _ in range(random.randint(1, 4)):
                question.tags.add(random.choice(tags))
        stdout_writer.stdout.write("Created test data: QUESTIONS")

    @classmethod
    def create_answers(cls):
        answers = []
        faker = Faker()
        users = LaskUser.objects.all()
        questions = Question.objects.all()
        for _ in range(ANSWERS_COUNT):
            answers.append(Answer(text=faker.text(),
                                  question=random.choice(questions),
                                  answer_author=random.choice(users),
                                  rating=random.randint(1, 100),
                                  ))
        Answer.objects.bulk_create(answers, ANSWERS_COUNT)
        stdout_writer.stdout.write("Created test data: ANSWERS")
