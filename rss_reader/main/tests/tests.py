# Default unittest test cases
from django.test import TestCase

# Model classes
from main.models import Feed, Post, Topic

# Built in users
from django.contrib.auth.models import User, UserManager

# Exception
from main.models import FeedURLInvalid
from django.db import IntegrityError

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback

#User tests
# class UserTestCase(TestCase):
#     def setUp(self):
#         self.u0 = RSSUser.objects.create_user('Devon','BAMF@uchicago.edu','login')
#
#     def test_create_user(self):
#         """ Test the user constructor is working """
#         # Create user
#         u1 = RSSUser.objects.create_user('Test','test@example.com','password')
#
#         # Make sure user exists
#         self.assertEquals(u1, RSSUser.objects.get(username='Test'))
#
#     def test_missing_user(self):
#         """create_user fails if missing username"""
#         def bad_user_input():
#             RSSUser.objects.create_user("","a","b")
#         self.assertRaises(ValueError, bad_user_input)
#
#     def test_missing_email(self):
#         """create_user fails if missing email"""
#         def bad_email_input():
#             RSSUser.objects.create_user("a","","b")
#         self.assertRaises(ValueError, bad_email_input)
#
#     def test_missing_password(self):
#         """create_user fails if missing password"""
#         def bad_password_input():
#             RSSUser.objects.create_user("a","b","")
#         self.assertRaises(ValueError, bad_password_input)
#
#     def test_usernames_unique(self):
#         """ Test that usernames must be unique """
#         def badCreate():
#             u1 = RSSUser.objects.create_user('Devon','BAMF@uchicago.edu','login')
#         self.assertRaises(IntegrityError, badCreate)
#
#     def test_emails_not_unique(self):
#         """ Test that emails don't have to be unique """
#         u1 = RSSUser.objects.create_user('Devon2','BAMF@uchicago.edu','login')
#         self.assertEqual(self.u0.email, u1.email)
#
#     def test_add_topic_to_user(self):
#         """ Can add a Topic to a user """
#         u1 = RSSUser.objects.get(username='Devon')
#         b1 = u1.addTopic("t1")
#
#         # Topic added to user
#         self.assertEqual(b1, True)
#         t1 = Topic.objects.get(name="t1")
#         self.assertEqual(t1.user.username,'Devon')

#     def test_topic_names_unique(self):
#         """ Cannot add Topic to user if there already exists a Topic of the same name """
#         u1 = RSSUser.objects.get(username='Devon')
#         u1.addTopic("t_first")
#         def badAddTopic():
#             u1.addTopic("t_first")
#         self.assertRaises(IntegrityError, badAddTopic)

#Topic tests
class TopicTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'login')
        self.u1.topics.create(name="t1")
        self.t1 = self.u1.topics.get(name="t1")
        self.u1.topics.create(name="t2")
        self.t2 = self.u1.topics.get(name="t2")
        self.f1 = Feed.createByUrl("http://home.uchicago.edu/~jharriman/example-rss.xml")
        self.f2 = Feed.createByUrl("http://xkcd.com/rss.xml")

    def test_minimal_topic(self):
        """Tests minimal data needed for Topic"""
        def wrap():
            exceptionRaised = False
            try:
                t = Topic(name="name")
            except Exception:
                exceptionRaised = True
            return exceptionRaised
        self.assertEqual(wrap(), False)

    def test_edit_topic_name(self):
        """editTopicName renames the topic"""
        b1 = self.t1.editTopicName("space")
        self.assertEqual(b1, True)
        self.assertEqual(self.t1.name, "space")

    def test_repeat_topic_name(self):
        """editTopicName throws an error if name already exists"""
        def repeat_topic():
            self.t1.editTopicName("t2")
        self.assertRaises(IntegrityError, repeat_topic())

    def test_add_feed(self):
        """ addFeed adds a Feed to a Topic """
        b1 = self.t1.addFeed(self.f1)
        self.assertEqual(b1, True)

        # adding Feed to topic it's already in should silently fail
        b1 = self.t1.addFeed(self.f1)
        self.assertEqual(b1, True)

        # cannot add Feed to two topics (f1 in t1 already)
        b1 = self.t2.addFeed(self.f1)
        self.assertEqual(b1, False)

    def test_delete_feed(self):
        """ deleteFeed deletes a Feed from a Topic """
        self.t1.addFeed(self.f1)
        self.t2.addFeed(self.f2)

        #feed not in topic
        b1 = self.t2.deleteFeed(self.f1)
        self.assertEqual(b1, False)

        #feed is in topic
        b1 = self.t1.deleteFeed(self.f1)
        self.assertEqual(b1, True)
        self.assertEqual(self.t1.feeds.all().exists(), False) #f1 deleted, queryset returned by feed_set.all is empty


class FeedTestCase(TestCase):
    def setUp(self):
        self.testUrl = "http://home.uchicago.edu/~jharriman/example-rss.xml"
        self.badUrl = "http://example.com"
        self.feed = Feed.createByUrl(self.testUrl)

    def test_create_by_url(self):
        """Constructor Feed.createByUrl accurately creates a Feed object"""
        feed = self.feed

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
        posts = feed.posts.all()
        post = posts[0]
        self.assertEqual(post.title, u"Bracing for the Falls of an Aging Nation")
        self.assertEqual(post.content, u'As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border="0" height="1" src="http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif" width="1" /><br clear="all" />')
        self.assertEqual(post.url, u"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm")
        self.assertEqual(post.pubDate, datetime.datetime(2014, 11, 2, 13, 43, 10, tzinfo=pytz.UTC))

        post = posts[1]
        self.assertEqual(post.title, u"Midterm Calculus: The Economy Elects Presidents. Presidents Elect Congress.")
        self.assertEqual(post.content, u"While presidential elections are shaped largely by economic performance, the largest factor in midterm elections is the president.")
        self.assertEqual(post.url,u"http://rss.nytimes.com/c/34625/f/642562/s/40134217/sc/1/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Cthe0Eeconomy0Eelects0Epresidents0Epresidents0Eelect0Econgress0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm")
        self.assertEqual(post.pubDate, datetime.datetime(2014, 11, 2, 14, 00, 22, tzinfo=pytz.UTC))

    def test_url_invalid(self):
        """ Test if a bad URL (non-feed) raises an invalid feed exception """
        def badFeedUrlCreation():
            feed = Feed.createByUrl(self.badUrl)
        self.assertRaises(FeedURLInvalid, badFeedUrlCreation)

    def test_minimal_feed(self):
        """ Test that we can create a feed with the minimal amount of data """
        def wrap():
            exceptionRaised = False
            try:
                f = Feed()
            except Exception:
                exceptionRaised = True
            return exceptionRaised
        self.assertEqual(wrap(), False)

    def test_get_posts(self):
        """ Test battery for getPosts """
        feed = self.feed
        posts = feed.getPosts(0)

        # 0
        self.assertEqual(feed.getPosts(0), [])

        # Greater than total number of cases
        self.assertEqual(feed.getPosts(3), list(feed.posts.all().order_by('-pubDate')))

        # Check posts equal
        self.assertEqual(feed.getPosts(1), feed.posts.all()[0])
        
        # Empty feed
        feed = Feed()
        self.assertEqual(feed.getPosts(1), [])


    def test_get_all(self):
        """ Test battery for getAll() """
        feed = self.feed

        # Test that the default test returns all its posts
        self.assertEqual(feed.getAll(), list(feed.posts.all()))

        # Test that it returns an empty list with an empty feed
        feed = Feed()
        self.assertEqual(feed.getAll(), [])

    def test_get_size(self):
        """ Test battery for getSize() """
        feed = self.feed

        # Test the actual feed size return
        self.assertEqual(feed.getSize(), 2)

        # Test 0 case
        feed = Feed()
        self.assertEqual(feed.getSize(), 0)

class PostTestCase(TestCase):
    def setUp(self):
        self.feed = Feed()
        self.feed.save()
        pass

    def test_create_post(self):
        """ Test post constructor createByEntry """
        entry_dict = {
            "author" : "Test",
            "tags" : [{"term" : "testCat"}],
            "rights" : "BARE ARMS",
            "title" : "Title",
            "subtitle" : "Subtitle",
            "summary" : "<h1>TEST</h1>",
            "generator" : "I don't know what this is",
            "id" : "www.example.com/1892",
            "link" : "www.example.com/1892",
            "contributor" : "Joe Smith",
            "published_parsed" : time.struct_time((2014, 11, 2, 16, 13, 2, 6, 306, 0)),
            "updated_parsed" : time.struct_time((2014, 11, 2, 16, 13, 2, 6, 306, 0))
        }

        # Create post
        post = Post.createByEntry(entry_dict, "www.example.com/test", self.feed)

        # Make sure all the fields are equal
        self.assertEqual(post.author, "Test")
        self.assertEqual(post.category, ["testCat"])
        self.assertEqual(post.rights, "BARE ARMS")
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.subtitle, "Subtitle")
        self.assertEqual(post.content, "<h1>TEST</h1>")
        self.assertEqual(post.generator, "I don't know what this is")
        self.assertEqual(post.guid, "www.example.com/1892")
        self.assertEqual(post.url, "www.example.com/1892")
        self.assertEqual(post.contributor, "Joe Smith")
        self.assertEqual(post.pubDate, datetime.datetime(2014, 11, 2, 14, 00, 22, tzinfo=pytz.UTC))
        self.assertEqual(post.updated_parsed, datetime.datetime(2014, 11, 2, 14, 00, 22, tzinfo=pytz.UTC))

    def test_post_no_feed(self):
        """ Test that we cannot create a post with the feed field = null"""
        def badPostConstruction():
            p = Post()
        self.assertRaises(IntegrityError, badPostConstruction())

    def test_minimal_post(self):
        """ Test that we can create a post with the minimal amount of data """
        f = Feed()
        def wrap():
            exceptionRaised = False
            try:
                p = Post({"feed" : f})
            except Exception:
                exceptionRaised = True
            return exceptionRaised
        self.assertEquals(wrap(), False)
