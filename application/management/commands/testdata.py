import time
import random
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from application.models import Question, Tag, Answer, LaskUser

USERS_COUNT = 100
QUESTIONS_COUNT = 500


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
            nick_name = random_name
            LaskUser.objects.create_user(username=login, email=email, password=_password, nick_name=nick_name)
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
        users = LaskUser.objects.all()
        tags = Tag.objects.all()
        titles_for_select = ("How do you handle source control?",
                             "What is abstraction with regards to.NET?",
                             "What’s your experience level with Eclipse or Visual Studio?",
                             "What is your advice when a client wants high performance, usability, and security?",
                             "How is a threat different from a vulnerability?",
                             "What does an intrusion detection system do? How does it do it?",
                             )
        text_for_select = (
            "You are working at a client site, and the CTO of the client company has asked if she can "
            "see you. The CTO wants to know how much it would cost to bring in five more people on your "
            "team. She gives you very vague requirements of the job she is looking for you to do. What "
            "would you do?",
            "You have been asked to research a new business tool. You have come across two solutions. "
            "One is an on-premise solution; the other is cloud-based. Assuming they are functionally "
            "equivalent, why would you recommend one over the other?",
            "You have submitted a piece of code that has broken the client's website in production. "
            "You have found this bug while you were testing, and nobody else knows about it. What is "
            "your next move?",
            "You have learned that a business unit is managing a major component of the business using "
            "Excel spreadsheets and Access databases. What risks does this present, and what would you "
            "recommend be done to mitigate these risks?",
            "When is the last time you downloaded a utility from the internet to make your work more productive, "
            "and what was it?",
        )
        for _ in range(QUESTIONS_COUNT):
            question = Question(title=random.choice(titles_for_select),
                                text=random.choice(text_for_select) * random.randint(1, 3),
                                question_author=random.choice(users),
                                rating=random.randint(1, 100),
                                )
            question.save()
            for _ in range(random.randint(1, 4)):
                question.tags.add(random.choice(tags))
        stdout_writer.stdout.write("Created test data: QUESTIONS")

    @classmethod
    def create_answers(cls):
        users = LaskUser.objects.all()
        questions = Question.objects.all()
        text_for_select = (
            "Also, review this list of common IT interview questions and take the time to prepare responses "
            "based on your qualifications for the job.",
            "se the STAR interview response technique to generate examples to share during the interview.",
            "Providing details will show the interviewer how and why you are qualified for the job. Do keep in "
            "mind that the questions you'll be asked will be specific to the job you're interviewing for, "
            "so they'll vary.",
            "Websites are available to help you practice responding to more technical questions. You may be asked "
            "during your interview to respond to technical questions using a whiteboard.",
        )
        for question in questions:
            for _ in range(random.randint(1, 100)):
                answer = Answer(text=random.choice(text_for_select) * random.randint(1, 3),
                                question=question,
                                answer_author=random.choice(users),
                                rating=random.randint(1, 100),
                                )
                answer.save()
        stdout_writer.stdout.write("Created test data: ANSWERS")
