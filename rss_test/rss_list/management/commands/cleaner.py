from django.core.management import BaseCommand

from rss_list.models import Feed

# clear whole database content
# usage: python manage.py cleaner


class Command(BaseCommand):
    def handle(self, *args, **options):
        f = Feed.objects.all()
        counter = len(f)
        f.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted "%s" feeds' % counter))