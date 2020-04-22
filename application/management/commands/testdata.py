import time
import random
from django.core.management.base import BaseCommand
from application.models import Question, Profile, Tag, Answer, User


# python manage.py testdata
class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **options):
        for i in range(5):
            pass


class TestDataForDb:
    @staticmethod
    def model_user(self):
        _password = "admin"
        names_for_login = 'Alex', 'Bob', 'Molomo', 'POPPY', 'James', 'Leo', 'Archie', 'Eva', 'Max'
        random_name = random.choice(names_for_login)
        login = random_name + f'({i})'
        email = random_name + f'({i})' + "@mail.ru"
        user = User.objects.create_user(login, email, _password)
        user.profile.nick_name = random_name
        user.save()