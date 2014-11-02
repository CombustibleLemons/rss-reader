from django.test import TestCase
from main.models import Feed, Post
import time

# Create your tests here.
class FeedTestCase(TestCase):
    def setUp(self):
        self.testUrl = "http://home.uchicago.edu/~jharriman/example-rss.xml"

    def testCreateByUrl(self):
        """Constructor Feed.createByUrl accurately creates a Feed object"""
        feed = Feed.createByUrl(self.testUrl)
        self.assertEqual(feed.URL, u"http://www.nytimes.com/services/xml/rss/nyt/US.xml")
        self.assertEqual(feed.language, u"en-us")
        self.assertEqual(feed.ttl, 5)

        # Dates Equal?
        pubTime = "2014-11-02T16:13:02Z"
        self.assertEqual(feed.pubDate, pubTime)

class PostTestCase(TestCase):
    def setUp(self):
        pass
