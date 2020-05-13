from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from .models import Answer
from .utilities import send_activation_notification, send_new_answer_notification

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


@receiver(post_save, sender=Answer)
def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].question.question_author
    if kwargs['created'] and author.send_messages:
        send_new_answer_notification(kwargs['instance'])
