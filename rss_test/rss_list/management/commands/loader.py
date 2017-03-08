from datetime import datetime
import feedparser
import ssl

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from rss_list.models import Feed

# Function to fetch the rss feed and store the parsed RSS into databse
# usage: python manage.py loader


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def to_date(value):
    try:
        return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        raise ValueError("invalid date %s" % value)


def store_single_feed(item):
    try:
        f = Feed.objects.get(link=item['link'])
    except ObjectDoesNotExist:
        f = Feed(title=item['title'], link=item['link'], pub_date=to_date(item['published']))
        f.save()
        return 1 # 'success'
    return 0     # 'feed already in database'


# Function grabs the rss feed headlines (titles, links, published dates) and save each to database
def getHeadlinesAndSave(rss_url):

    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = parseRSS(rss_url)
    counter = 0
    for newsitem in feed['items']:
        counter += store_single_feed(newsitem)
    return counter # succesfully added feeds number


# List of RSS feeds that we will fetch and combine
newsurls = {
    'djangonews': 'https://www.djangoproject.com/rss/weblog/',
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Iterate over the feed urls
        counter = 0
        for key, url in newsurls.items():
            counter += getHeadlinesAndSave(url)

        self.stdout.write(self.style.SUCCESS('Successfully added "%s" feeds' % counter))