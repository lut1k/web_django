import time
import random
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from application.models import Question, Tag, Answer, User

USERS_COUNT = 20
QUESTIONS_COUNT = 100
ANSWERS_COUNT = 100


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
        stdout_writer.stdout.write("Created test data: USERS")

    @classmethod
    def create_tags(cls):
        tags_for_select = ("HTML", "IT", "CSS", "Python", "Django", "JS", "Junior", "C++", "C#")
        for tag in tags_for_select:
            tag = Tag(name=tag)
            try:
                tag.save()
            except IntegrityError:
                continue
        stdout_writer.stdout.write("Created test data: TAGS")

    @classmethod
    def create_questions(cls):
        users = User.objects.all()
        tags = Tag.objects.all()
        titles_for_select = ("How do you handle source control?",
                             "What is abstraction with regards to.NET?",
                             "What’s your experience level with Eclipse or Visual Studio?",
                             "What is your advice when a client wants high performance, usability, and security?",
                             "How is a threat different from a vulnerability?",
                             "What does an intrusion detection system do? How does it do it?",
                             )
        text_for_select = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
                          "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud " \
                          "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure " \
                          "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
                          "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt " \
                          "mollit anim id est laborum."
        for _ in range(QUESTIONS_COUNT):
            question = Question(title=random.choice(titles_for_select),
                                text=text_for_select * random.randint(1, 4),
                                question_author=random.choice(users),
                                rating=random.randint(1, 100),
                                )
            question.save()
            for _ in range(random.randint(1, 4)):
                question.tags.add(random.choice(tags))
        stdout_writer.stdout.write("Created test data: QUESTIONS")

    @classmethod
    def create_answers(cls):
        users = User.objects.all()
        questions = Question.objects.all()
        text_for_select = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
                          "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud " \
                          "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure " \
                          "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
                          "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt " \
                          "mollit anim id est laborum."
        for question in questions:
            answer = Answer(text=text_for_select * random.randint(1, 4),
                            question=question,
                            answer_author=random.choice(users),
                            rating=random.randint(1, 100),
                            )
            answer.save()
        stdout_writer.stdout.write("Created test data: ANSWERS")





