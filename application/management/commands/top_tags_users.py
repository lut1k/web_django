from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Prepares data for the right column (best users, popular tags). ' \
           'Popular Tags - these are 10 tags with the most questions in the last 3 months. ' \
           'The best users are the users with the most questions + answers in the last 3 months.'

    def handle(self, *args, **options):
        pass
