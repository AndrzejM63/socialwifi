from django.core.management import BaseCommand

from rss_list.models import Feed

# clear whole database content
# usage: python manage.py cleaner


class Command(BaseCommand):
    def handle(self, *args, **options):
        f = Feed.objects.all()
        _, deleted_dict = f.delete()
        counter = deleted_dict['rss_list.Feed']
        self.stdout.write(self.style.SUCCESS('Successfully deleted "%s" feeds' % counter))