# Default unittest test cases
from django.test import TestCase

# Model classes
from main.models import UserSettings, Feed, Post, RSS, Atom, Topic

# Built in users
from django.contrib.auth.models import User, UserManager

## Transaction Management
from django.db import transaction

# Exception
from main.models import FeedURLInvalid, FeedExistsInTopic
from django.db import IntegrityError

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback
import feedparser

#UserSettings tests
class UserSettingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'login')
        self.user.save()
        self.settings = UserSettings(user=self.user)

    def tearDown(self):
        self.user.delete()
        self.settings.delete()

    def test_readtime_default(self):
        self.assertEqual(self.user.settings.readtime, 300)

    def change_readtime_exists(self):
        self.user.settings.readTime = 400
        self.assertEqual(self.user.settings.readtime, 400)

#Topic tests
class TopicTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # User
        cls.u1 = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'login')

        # Feed 1
        cls.f1 = Feed.createByURL("http://home.uchicago.edu/~jharriman/example-rss.xml")
        cls.f1.save()

        # Feed 2
        cls.f2 = Feed.createByURL("http://xkcd.com/rss.xml")
        cls.f2.save()

    @classmethod
    def tearDownClass(cls):
        cls.f1.delete()
        cls.f2.delete()
        User.objects.get(username="Devon").delete()

    def setUp(self):
        # Create topic t1
        self.u1.topics.create(name="t1")
        self.t1 = self.u1.topics.get(name="t1")
        self.t1.save()

        # Create topic t2
        self.u1.topics.create(name="t2")
        self.t2 = self.u1.topics.get(name="t2")
        self.t2.save()

    def tearDown(self):
        self.t1.delete()
        self.t2.delete()

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
        self.assertEqual(self.t1.name, "space")

    def test_repeat_topic_name(self):
        """editTopicName throws an error if name already exists"""
        def repeat_topic():
            with transaction.atomic():
                self.t1.editTopicName("t2")
        self.assertRaises(IntegrityError, repeat_topic)

    def test_add_feed(self):
        """ addFeed adds a Feed to a Topic """
        b1 = self.t1.addFeed(self.f1)
        self.assertEqual(self.t1.feeds.all()[0], self.f1)

        # adding Feed to topic it's already in should silently fail
        b1 = self.t1.addFeed(self.f1)
        self.assertEqual(self.t1.feeds.all()[0], self.f1)
        self.assertEqual(len(self.t1.feeds.all()), 1)

    def test_other_topic_has_feed(self):
        """ Cannot add Feed to two topics """
        self.t1.addFeed(self.f1)
        def other_topic():
            self.t2.addFeed(self.f1)
        self.assertRaises(FeedExistsInTopic, other_topic)

    def test_delete_feed(self):
        """ deleteFeed deletes a Feed from a Topic """
        self.t1.addFeed(self.f1)
        self.t2.addFeed(self.f2)

        #feed not in topic, should fail silently
        b1 = self.t2.deleteFeed(self.f1)
        self.assertEqual(len(self.t2.feeds.all()), 1)
        self.assertEqual(self.t2.feeds.all()[0], self.f2)

        #feed is in topic
        b1 = self.t1.deleteFeed(self.f1)
        self.assertEqual(self.t1.feeds.all().exists(), False) #QuerySet of feeds is empty


class FeedTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rssFeed = Feed.createByURL("main/tests/examples/rss20.xml")
        cls.rssFeed.save()
        cls.atomFeed = Feed.createByURL("main/tests/examples/atom10.xml")
        cls.rssFeed.save()
        cls.badUrl = "http://example.com"

    @classmethod
    def tearDownClass(cls):
        cls.rssFeed.delete()
        cls.atomFeed.delete()

    def test_create_by_url_atom(self):
        """Constructor Feed.createByURL accurately creates a Feed object"""
        feed = self.atomFeed

        # Check Feed fields
        self.assertEqual(feed.URL, u"main/tests/examples/atom10.xml")
        self.assertEqual(feed.docURL, u"") # Feedparser seems to be failing on this one
        self.assertEqual(feed.language, u"")
        self.assertEqual(feed.ttl, None)
        self.assertEqual(feed.title, u"Sample Feed")
        self.assertEqual(feed.subtitle, u"For documentation &lt;em&gt;only&lt;/em&gt;")
        self.assertEqual(feed.rights, u"&lt;p>Copyright 2005, Mark Pilgrim&lt;/p>")
        self.assertEqual(feed.logo, u"")
        # Dates Equal?
        # pubTime = "2002-09-07T00:00:00Z"
        # self.assertEqual(feed.pubDate, pubTime)
        # self.assertEqual(feed.updated, pubTime)

        # Check each of the Posts
        posts = feed.posts.all()
        post = posts[0]
        self.assertEqual(post.author, u"Mark Pilgrim (mark@example.org)")
        self.assertEqual(post.category, [])
        self.assertEqual(post.rights, u"")
        self.assertEqual(post.title, u"First entry title")
        self.assertEqual(post.subtitle, "")
        self.assertEqual(post.content, u"Watch out for nasty tricks")
        self.assertEqual(post.generator, u"")
        self.assertEqual(post.guid, u"tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3")
        self.assertEqual(post.url, u"")
        self.assertEqual(post.contributor, u"")
        self.assertEqual(post.updated, datetime.datetime(2005, 11, 9, 11, 56, 34, tzinfo=pytz.UTC))
        self.assertEqual(post.pubDate, datetime.datetime(2005, 11, 9, 0, 23, 47, tzinfo=pytz.UTC))

    def test_create_by_url_rss(self):
        """Constructor Feed.createByURL accurately creates a Feed object"""
        feed = self.rssFeed

        # Check Feed fields
        self.assertEqual(feed.URL, u"main/tests/examples/rss20.xml")
        self.assertEqual(feed.docURL, u"http://example.org/")
        self.assertEqual(feed.language, u"en")
        self.assertEqual(feed.ttl, 60)
        self.assertEqual(feed.title, u"Sample Feed")
        self.assertEqual(feed.subtitle, u"For documentation <em>only</em>")
        self.assertEqual(feed.rights, u"Copyright 2004, Mark Pilgrim")
        self.assertEqual(feed.logo, u"http://example.org/banner.png")
        # Dates Equal?
        pubTime = "2002-09-07T00:00:00Z"
        self.assertEqual(feed.pubDate, pubTime)
        # self.assertEqual(feed.updated, pubTime)

        # Check each of the Posts
        post = feed.posts.all()[0]

        # Make sure all the fields are equal
        self.assertEqual(post.author, u"mark@example.org")
        self.assertEqual(post.category, [u"Miscellaneous"])
        self.assertEqual(post.rights, u"")
        self.assertEqual(post.title, u"First item title")
        self.assertEqual(post.subtitle, "")
        self.assertEqual(post.content, u"Watch out for <span> nasty tricks</span>")
        self.assertEqual(post.generator, u"")
        self.assertEqual(post.guid, u"http://example.org/guid/1")
        self.assertEqual(post.url, u"http://example.org/item/1")
        self.assertEqual(post.contributor, u"")
        self.assertEqual(post.updated, datetime.datetime(2002, 9, 5, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(post.pubDate, datetime.datetime(2002, 9, 5, 0, 0, tzinfo=pytz.UTC))

        # # RSS Specific fields
        # self.assertEqual(post.enclosure, ["http://example.org/audio/demo.mp3"])
        # self.assertEqual(post.comments, "http://example.org/comments/1")
        #
        # # Make sure it doesn't contain Atom specific fields
        # def checkAtomNotPresent():
        #     post.summary()
        # self.assertRaises(KeyError, checkAtomNotPresent)

    def test_url_invalid(self):
        """ Test if a bad URL (non-feed) raises an invalid feed exception """
        def badFeedUrlCreation():
            feed = Feed.createByURL(self.badUrl)
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
        feed = self.rssFeed
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
        feed = self.rssFeed

        # Test that the default test returns all its posts
        self.assertEqual(feed.getAll(), list(feed.posts.all()))

        # Test that it returns an empty list with an empty feed
        feed = Feed()
        self.assertEqual(feed.getAll(), [])

    def test_get_size(self):
        """ Test battery for getSize() """
        feed = self.rssFeed

        # Test the actual feed size return
        self.assertEqual(feed.getSize(), 1)

        # Test 0 case
        feed = Feed()
        self.assertEqual(feed.getSize(), 0)

class PostTestCase(TestCase):
    def setUp(self):
        self.feed = Feed()
        self.feed.save()
    # Dont' think we need this if we are making the Post a virtual field
    # def test_create_post(self):
    #     """ Test post constructor createByEntry """
    #     entry_dict = {
    #         "author" : "Test",
    #         "tags" : [{"term" : "testCat"}],
    #         "rights" : "BARE ARMS",
    #         "title" : "Title",
    #         "subtitle" : "Subtitle",
    #         "summary" : "<h1>TEST</h1>",
    #         "generator" : "I don't know what this is",
    #         "id" : "www.example.com/1892",
    #         "link" : "www.example.com/1892",
    #         "contributor" : "Joe Smith",
    #         "published_parsed" : time.struct_time((2014, 11, 2, 16, 13, 2, 6, 306, 0)),
    #         "updated_parsed" : time.struct_time((2014, 11, 2, 16, 13, 2, 6, 306, 0))
    #     }
    #
    #     # Create post
    #     post = Post.createByEntry(entry_dict, "www.example.com/test", self.feed)
    #
    #     # Make sure all the fields are equal
    #     self.assertEqual(post.author, "Test")
    #     self.assertEqual(post.category, ["testCat"])
    #     self.assertEqual(post.rights, "BARE ARMS")
    #     self.assertEqual(post.title, "Title")
    #     self.assertEqual(post.subtitle, "Subtitle")
    #     self.assertEqual(post.content, "<h1>TEST</h1>")
    #     self.assertEqual(post.generator, "I don't know what this is")
    #     self.assertEqual(post.guid, "www.example.com/1892")
    #     self.assertEqual(post.url, "www.example.com/1892")
    #     self.assertEqual(post.contributor, "Joe Smith")
    #     self.assertEqual(post.updated, datetime.datetime(2014, 11, 2, 14, 00, 22, tzinfo=pytz.UTC))
    #     self.assertEqual(post.pubDate, datetime.datetime(2014, 11, 2, 14, 00, 22, tzinfo=pytz.UTC))

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

class RSSTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a feed to put the post in, since the post must have a feed.
        cls.feed = Feed()
        cls.feed.save()

        # Grab an entry and parse it
        cls.entry = feedparser.parse("main/tests/examples/rss20.xml")["entries"][0]

    @classmethod
    def tearDownClass(cls):
        cls.feed.delete()

    def test_create_rss(self):
        """ Test RSS constructor createByEntry """
        # Create post
        post = RSS.createByEntry(self.entry, "http://www.example.org/atom10.xml", self.feed)
        post.save()
        post = Post.objects.get(id=post.id)

        # Make sure all the fields are equal
        self.assertEqual(post.author, u"mark@example.org")
        self.assertEqual(post.category, [u"Miscellaneous"])
        self.assertEqual(post.rights, u"")
        self.assertEqual(post.title, u"First item title")
        self.assertEqual(post.subtitle, "")
        self.assertEqual(post.content, u"Watch out for <span> nasty tricks</span>")
        self.assertEqual(post.generator, u"")
        self.assertEqual(post.guid, u"http://example.org/guid/1")
        self.assertEqual(post.url, u"http://example.org/item/1")
        self.assertEqual(post.contributor, u"")
        self.assertEqual(post.updated, datetime.datetime(2002, 9, 5, 0, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(post.pubDate, datetime.datetime(2002, 9, 5, 0, 0, 0, tzinfo=pytz.UTC))

        # # RSS Specific fields
        # self.assertEqual(post.enclosure, ["http://example.org/audio/demo.mp3"])
        # self.assertEqual(post.comments, "http://example.org/comments/1")

    def test_post_no_feed(self):
        """ Test that we cannot create a post with the feed field = null"""
        def badPostConstruction():
            p = RSS()
        self.assertRaises(IntegrityError, badPostConstruction())

    def test_minimal_post(self):
        """ Test that we can create a post with the minimal amount of data """
        f = Feed()
        def wrap():
            exceptionRaised = False
            try:
                p = RSS({"feed" : f})
            except Exception:
                exceptionRaised = True
            return exceptionRaised
        self.assertEquals(wrap(), False)
