import datetime
from django.test import TestCase
from freezegun import freeze_time

# Create your tests here.

from rss_list.management.commands.loader import to_date, store_single_feed
from rss_list.models import Feed

# correct feeds
feed1 = { 'title': 'a', 'link': 'b', 'published': 'Wed, 01 Mar 2017 07:25:58 -0600'}
feed2 = { 'title': 'b', 'link': 'c', 'published': 'Wed, 01 Apr 2017 07:25:58 -0600'}
feed3 = { 'title': 'c', 'link': 'd', 'published': 'Wed, 01 May 2017 07:25:58 -0600'}

# incorrect feeds
feed_wrong_date = { 'title': 'c', 'link': 'e', 'published': 'Wed, 31 Feb 2017 07:25:58 -0600'}
feed_empty_date = { 'title': 'd', 'link': 'f', 'published': ''}
feed_naive_date = { 'title': 'e', 'link': 'g', 'published': 'Wed, 28 Feb 2017 07:25:58'}

class DateStringConvertionToDatetimeCase(TestCase):
    def test_expected_date_format_strings(self):
        self.assertEqual(to_date(feed1['published']),
                         datetime.datetime.strptime(feed1['published'], "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None))

    def test_wrong_date(self):
        with freeze_time("2017-03-09"):
            self.assertEqual(to_date(feed_wrong_date['published']), datetime.datetime.now(tz=None))

    def test_empty_date(self):
        with freeze_time("2017-03-09"):
            self.assertEqual(to_date(feed_empty_date['published']), datetime.datetime.now(tz=None))

    def test_naive_date(self):
        with freeze_time("2017-03-09"):
            self.assertEqual(to_date(feed_naive_date['published']), datetime.datetime.now(tz=None))


class FeedTestCase(TestCase):
    def setUp(self):
        Feed.objects.create(title=feed1['title'], link=feed1['link'], pub_date=to_date(feed1['published']))
        Feed.objects.create(title=feed2['title'], link=feed2['link'], pub_date=to_date(feed2['published']))

    def test_adding_single_feeds(self):
        # add new feed3 to database
        self.assertTrue(store_single_feed(feed3))

    def test_adding_existing_feeds(self):
        # add existing feed3 to database
        self.assertFalse(store_single_feed(feed1))

