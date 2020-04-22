import time
import random
from django.core.management.base import BaseCommand
from application.models import Question, Profile, Tag, Answer, User

USERS_COUNT = 1
QUESTIONS_COUNT = 1
ANSWERS_COUNT = 1
TAGS_COUNT = 1


# python manage.py testdata
class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **options):
        TestDataForDb.create_users()
        self.stdout.write("Created test data: users")


class TestDataForDb:
    @classmethod
    def create_users(cls):
        _password = "admin"
        names_for_login = 'Alex', 'Bob', 'Molomo', 'POPPY', 'James', 'Leo', 'Archie', 'Eva', 'Max'
        for _ in range(USERS_COUNT):
            postfix_time = f'_{time.time()}'
            random_name = random.choice(names_for_login)
            login = random_name + postfix_time
            email = random_name + postfix_time + "@mail.ru"
            user = User.objects.create_user(login, email, _password)
            user.profile.nick_name = random_name
            user.save()

    @classmethod
    def create_questions(cls):
        pass

    @classmethod
    def create_answers(cls):
        pass

    @classmethod
    def create_tags(cls):
        pass

