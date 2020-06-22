from django.core.management import BaseCommand
from django.db.models import Count
from application.models import Tag, LaskUser


class Command(BaseCommand):
    help = 'Prepares data for the right column (best users, popular tags). ' \
           'Popular Tags - these are 10 tags with the most questions in the last 3 months. ' \
           'The best users are the users with the most questions + answers in the last 3 months.'

    def handle(self, *args, **options):
        self.top_tags()
        self.top_users()

    @classmethod
    def top_tags(cls):
        tags = Tag.objects.annotate(count=Count('question')).order_by('-count')[:5]
        return tags

    @classmethod
    def top_users(cls):
        users = LaskUser.objects.all()[:5]
        return users
