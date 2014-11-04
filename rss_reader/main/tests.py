from django.test import TestCase
from main.models import Feed, Post
import time
import datetime
import pytz

# Create your tests here.
class FeedTestCase(TestCase):
    def setUp(self):
        self.testUrl = "http://home.uchicago.edu/~jharriman/example-rss.xml"

    def test_create_by_url(self):
        """Constructor Feed.createByUrl accurately creates a Feed object"""
        feed = Feed.createByUrl(self.testUrl)

        # Check Feed fields
        self.assertEqual(feed.URL, u"http://www.nytimes.com/services/xml/rss/nyt/US.xml")
        self.assertEqual(feed.language, u"en-us")
        self.assertEqual(feed.ttl, 5)
        self.assertEqual(feed.title, u"NYT > U.S.")
        self.assertEqual(feed.subtitle, u"US")
        self.assertEqual(feed.rights, u"Copyright 2014 The New York Times Company")
        self.assertEqual(feed.logo, u"http://graphics8.nytimes.com/images/misc/NYT_logo_rss_250x40.png")
        # Dates Equal?
        pubTime = "2014-11-02T16:13:02Z"
        self.assertEqual(feed.pubDate, pubTime)
        # self.assertEqual(feed.updated, pubTime)

        # Check each of the Posts
        posts = feed.post_set.all()
        post = posts[0]
        self.assertEqual(post.title, u"Bracing for the Falls of an Aging Nation")
        self.assertEqual(post.content, u'As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border="0" height="1" src="http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif" width="1" /><br clear="all" />')
        self.assertEqual(post.url, u"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm")
        self.assertEqual(post.pubDate, datetime.datetime(2014, 11, 2, 13, 43, 10, tzinfo=pytz.UTC))

class PostTestCase(TestCase):
    def setUp(self):
        pass
