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

        post = posts[1]
        self.assertEqual(post.title. u"Midterm Calculus: The Economy Elects Presidents. Presidents Elect Congress.")

class PostTestCase(TestCase):
    def setUp(self):
        pass

#User tests
class UserTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('Devon','BAMF@uchicago.edu','login')

    def test_addTopic(self):
        """addTopic(self) adds a Topic if it does not already exist"""
        b1 = u1.addTopic("t1")

        self.assertEqual(b1, True)
        self.assertEqual(u1.topic_set.all(), "[<Topic: t1>]")

        b2 = u1.addTopic("t1")
        self.assertEqual(b2, False)
        self.assertEqual(u1.topic_set.all(), "[<Topic: t1>]")

        b3 = u1.addTopic("t2")
        self.assertEqual(b3,True)
        self.assertEqual(u1.topic_set.all(), "[<Topic: t1>, <Topic: t2>]")

        # TEST FOR WEIRDO TOPIC NAMES?!

#Topic tests
class TopicTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'login')
        u1.addTopic("t1")
        t1 = u1.topic_set.get(name="t1")
        u1.addTopic("t2")
        t2 = u1.topic_set.get(name="t2")
        f1 = "PRETEND THIS IS A FEED FOR NOW"
        f2 = "AND ANOTHER"

    def test_editTopicName(self):
        b1 = t1.editTopicName("space")
        self.assertEqual(b1, True)
        self.assertEqual(t1.name, "space")
        # test for dealing with weird topic names

    def test_addFeed(self):
        b1 = t1.addFeed(f1)
        self.assertEqual(b1, True)
        # adding feed to topic its already in should silently fail
        b1 = t1.addFeed(f1)
        self.assertEqual(b1, True)
        b1 = t2.addFeed(f1)
        self.assertEqual(b1, False)

    def test_deleteFeed(self):
        t1.addFeed(f1)
        t1.addFeed(f2)

        b1 = t2.deleteFeed(f1)
        self.assertEqual(b1, False)
        b1 = t1.deleteFeed(f1)
        self.assertEqual(b1, True)
        self.assertEqual(t1.feed_set.all(), "[<Feed: FEEDIDENTIFIER?>]"
        b1 = t2.deleteFeed(f1)
        self.assertEqual(b1,False)