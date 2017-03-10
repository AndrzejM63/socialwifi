import datetime
import feedparser
import ssl
from urllib import request

from django.core.management import BaseCommand
from rss_list.models import Feed

# Function to fetch the rss feed and store the parsed RSS into databse
# usage: python manage.py loader


def parse_rss(rss_url):
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
        handlers = [request.HTTPSHandler(context=context)]
    else:
        handlers = []
    return feedparser.parse(rss_url, handlers=handlers)


def to_date(value):
    try:
        t = datetime.datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        t = datetime.datetime.now()
    naive = t.replace(tzinfo=None)    # this is because of MySQL connector bug = MySQL do not support timezone
    return naive


def store_single_feed(item):
    _, created = Feed.objects.get_or_create(
        link=item['link'],
        defaults={'title': item['title'], 'pub_date': to_date(item['published'])},
    )
    return created


# Function grabs the rss feed headlines (titles, links, published dates) and save each to database
def get_headlines_and_save(rss_url):
    feed = parse_rss(rss_url)
    counter = 0
    for newsitem in feed['items']:
        counter += store_single_feed(newsitem)
    return counter # succesfully added feeds number


# List of RSS feeds that we will fetch and combine
NEWS_URLS = {
    'djangonews': 'https://www.djangoproject.com/rss/weblog/',
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Iterate over the feed urls
        counter = 0
        for url in NEWS_URLS.values():
            counter += get_headlines_and_save(url)

        self.stdout.write(self.style.SUCCESS('Successfully added "%s" feeds' % counter))