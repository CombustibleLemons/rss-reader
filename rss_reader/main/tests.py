from django.test import TestCase
from main.models import Feed, Post

# Create your tests here.
class FeedTestCase(TestCase):
    def setUp(self):
        self.testUrl = "http://home.uchicago.edu/~jharriman/example-rss.xml"

    def testCreateByUrl(self):
        """Test that createByUrl constructor accurately creates a Feed object"""
        feed = Feed.createByUrl(self.testUrl)
        self.assertEqual(feed.URL, "http://rss.nytimes.com/services/xml/rss/nyt/US.xml")

class PostTestCase(TestCase):
    def setUp(self):
        pass
