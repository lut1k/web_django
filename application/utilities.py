import os
from datetime import datetime
from os.path import splitext
from django.core.signing import Signer
from django.template.loader import render_to_string
from web_django.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[3]
    else:
        host = 'http://localhost:8000'
    context = {'user': user,
               'host': host,
               'sign': signer.sign(user.username)
               }
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def send_new_answer_notification(answer):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[3]
    else:
        host = 'http://localhost:8000'
    user = answer.question.question_author
    question = answer.question
    context = {'user': user,
               'host': host,
               'answer': answer,
               'question': question,
               }
    subject = render_to_string('email/new_answer_letter_subject.txt', context)
    body_text = render_to_string('email/new_answer_letter_body.txt', context)
    user.email_user(subject, body_text)


def get_user_directory_path(instance, filename):
    return os.path.join("user_{}".format(instance.id), "{}{}".format(datetime.now().timestamp(), splitext(filename)[1]))
