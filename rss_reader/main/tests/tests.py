# Default unittest test cases
from django.test import TestCase

# Model classes
from main.models import *
#UserSettings, Feed, QueueFeed, Post, RSS, Atom, Topic

# Built in users
from django.contrib.auth.models import User, UserManager

## Transaction Management
from django.db import transaction

# Exception
from main.models import FeedURLInvalid, FeedExistsInTopic
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Python built-ins required for tests
import time
import datetime
import timedelta
import pytz
import traceback
import feedparser
from django.utils import timezone

#UserSettings tests
# class UserSettingsTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user('Lucia', 'lucialu94@uchicago.edu', 'login')
#         self.user.save()
#
#     def tearDown(self):
#         self.user.delete()
#
#     def settings_exist(self):
#         """Users are created with settings"""
#         self.assertEqual(self.user.settings.exists(), True)
#
#     def test_readtime_default(self):
#         """Default readtime is 300"""
#         self.assertEqual(self.user.settings.readtime, 300)
#
#     def change_readtime_exists(self):
#         """Changing the readtime should work"""
#         self.user.settings.readTime = 400
#         self.assertEqual(self.user.settings.readtime, 400)

#Topic tests
# class TopicTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # User
#         cls.u1 = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'login')
#         cls.u1.save()
#
#         # Feed 1
#         cls.f1 = Feed.createByURL("http://home.uchicago.edu/~jharriman/example-rss.xml")
#         cls.f1.save()
#
#         # Feed 2
#         cls.f2 = Feed.createByURL("http://xkcd.com/rss.xml")
#         cls.f2.save()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.f1.delete()
#         cls.f2.delete()
#         cls.u1.delete()
#
#     def setUp(self):
#         # Create topic t1
#         self.u1.topics.create(name="t1")
#         self.t1 = self.u1.topics.get(name="t1")
#         self.t1.save()
#
#         # Create topic t2
#         self.u1.topics.create(name="t2")
#         self.t2 = self.u1.topics.get(name="t2")
#         self.t2.save()
#
#     def tearDown(self):
#         self.t1.delete()
#         self.t2.delete()
#
#     def test_minimal_topic(self):
#         """Tests minimal data needed for Topic"""
#         def wrap():
#             exceptionRaised = False
#             try:
#                 t = Topic(name="name")
#             except Exception:
#                 exceptionRaised = True
#             return exceptionRaised
#         self.assertEqual(wrap(), False)
#
#     def test_edit_topic_name(self):
#         """editTopicName renames the topic"""
#         self.t1.editTopicName("space")
#         self.assertEqual(self.t1.name, "space")
#
#     def test_repeat_topic_name(self):
#         """editTopicName throws an error if name already exists"""
#         def repeat_topic():
#             with transaction.atomic():
#                 self.t1.editTopicName("t2")
#         self.assertRaises(IntegrityError, repeat_topic)
#
#     def test_add_feed(self):
#         """ adds a Feed to a Topic """
#         self.t1.feeds.add(self.f1)
#         self.assertEqual(self.t1.feeds.all()[0], self.f1)
#
#         # adding Feed to topic it's already in should silently fail
#         self.t1.feeds.add(self.f1)
#         self.assertEqual(self.t1.feeds.all()[0], self.f1)
#         self.assertEqual(len(self.t1.feeds.all()), 1)
#
#     def test_other_topic_has_feed(self):
#         """ Cannot add Feed to two topics """
#         self.t1.feeds.add(self.f1)
#         def other_topic():
#             self.t2.feeds.add(self.f1)
#         self.assertRaises(ValidationError, other_topic)
#
#     def test_delete_feed(self):
#         """ deleteFeed deletes a Feed from a Topic """
#         self.t1.feeds.add(self.f1)
#         self.t2.feeds.add(self.f2)
#
#         #feed not in topic, should fail silently
#         self.t2.deleteFeed(self.f1)
#         self.assertEqual(len(self.t2.feeds.all()), 1)
#         self.assertEqual(self.t2.feeds.all()[0], self.f2)
#
#         #feed is in topic
#         b1 = self.t1.deleteFeed(self.f1)
#         self.assertEqual(self.t1.feeds.all().exists(), False) #QuerySet of feeds is empty


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

    # def test_create_by_url_atom(self):
    #     """Constructor Feed.createByURL accurately creates a Feed object"""
    #     feed = self.atomFeed
    #
    #     # Check Feed fields
    #     self.assertEqual(feed.URL, u"main/tests/examples/atom10.xml")
    #     self.assertEqual(feed.docURL, u"") # Feedparser seems to be failing on this one
    #     self.assertEqual(feed.language, u"")
    #     self.assertEqual(feed.ttl, None)
    #     self.assertEqual(feed.title, u"Sample Feed")
    #     self.assertEqual(feed.subtitle, u"For documentation &lt;em&gt;only&lt;/em&gt;")
    #     self.assertEqual(feed.rights, u"&lt;p>Copyright 2005, Mark Pilgrim&lt;/p>")
    #     self.assertEqual(feed.logo, u"")
    #     # Dates Equal?
    #     # pubTime = "2002-09-07T00:00:00Z"
    #     # self.assertEqual(feed.pubDate, pubTime)
    #     # self.assertEqual(feed.updated, pubTime)
    #
    #     # Check each of the Posts
    #     posts = feed.posts.all()
    #     post = posts[0]
    #     self.assertEqual(post.author, u"Mark Pilgrim (mark@example.org)")
    #     self.assertEqual(post.category, [])
    #     self.assertEqual(post.rights, u"")
    #     self.assertEqual(post.title, u"First entry title")
    #     self.assertEqual(post.subtitle, "")
    #     self.assertEqual(post.content, u"Watch out for nasty tricks")
    #     self.assertEqual(post.generator, u"")
    #     self.assertEqual(post.guid, u"tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3")
    #     self.assertEqual(post.url, u"")
    #     self.assertEqual(post.contributor, u"")
    #     self.assertEqual(post.updated, datetime.datetime(2005, 11, 9, 11, 56, 34, tzinfo=pytz.UTC))
    #     self.assertEqual(post.pubDate, datetime.datetime(2005, 11, 9, 0, 23, 47, tzinfo=pytz.UTC))

    # def test_create_by_url_rss(self):
    #     """Constructor Feed.createByURL accurately creates a Feed object"""
    #     feed = self.rssFeed
    #
    #     # Check Feed fields
    #     self.assertEqual(feed.URL, u"main/tests/examples/rss20.xml")
    #     self.assertEqual(feed.docURL, u"http://example.org/")
    #     self.assertEqual(feed.language, u"en")
    #     self.assertEqual(feed.ttl, 60)
    #     self.assertEqual(feed.title, u"Sample Feed")
    #     self.assertEqual(feed.subtitle, u"For documentation <em>only</em>")
    #     self.assertEqual(feed.rights, u"Copyright 2004, Mark Pilgrim")
    #     self.assertEqual(feed.logo, u"http://example.org/banner.png")
    #     # Dates Equal?
    #     pubTime = "2002-09-07T00:00:00Z"
    #     self.assertEqual(feed.pubDate, pubTime)
    #     # self.assertEqual(feed.updated, pubTime)
    #
    #     # Check each of the Posts
    #     post = feed.posts.all()[0]
    #
    #     # Make sure all the fields are equal
    #     self.assertEqual(post.author, u"mark@example.org")
    #     self.assertEqual(post.category, [u"Miscellaneous"])
    #     self.assertEqual(post.rights, u"")
    #     self.assertEqual(post.title, u"First item title")
    #     self.assertEqual(post.subtitle, "")
    #     self.assertEqual(post.content, u"Watch out for <span> nasty tricks</span>")
    #     self.assertEqual(post.generator, u"")
    #     self.assertEqual(post.guid, u"http://example.org/guid/1")
    #     self.assertEqual(post.url, u"http://example.org/item/1")
    #     self.assertEqual(post.contributor, u"")
    #     self.assertEqual(post.updated, datetime.datetime(2002, 9, 5, 0, 0, tzinfo=pytz.UTC))
    #     self.assertEqual(post.pubDate, datetime.datetime(2002, 9, 5, 0, 0, tzinfo=pytz.UTC))
    #
    #     # # RSS Specific fields
    #     # self.assertEqual(post.enclosure, ["http://example.org/audio/demo.mp3"])
    #     # self.assertEqual(post.comments, "http://example.org/comments/1")
    #     #
    #     # # Make sure it doesn't contain Atom specific fields
    #     # def checkAtomNotPresent():
    #     #     post.summary()
    #     # self.assertRaises(KeyError, checkAtomNotPresent)

    # def test_url_invalid(self):
    #     """ Test if a bad URL (non-feed) raises an invalid feed exception """
    #     def badFeedUrlCreation():
    #         feed = Feed.createByURL(self.badUrl)
    #     self.assertRaises(FeedURLInvalid, badFeedUrlCreation)

    # def test_minimal_feed(self):
    #     """ Test that we can create a feed with the minimal amount of data """
    #     def wrap():
    #         exceptionRaised = False
    #         try:
    #             f = Feed()
    #         except Exception:
    #             exceptionRaised = True
    #         return exceptionRaised
    #     self.assertEqual(wrap(), False)

    # def test_get_posts(self):
    #     """ Test battery for getPosts """
    #     feed = self.rssFeed
    #     posts = feed.getPosts(0)
    #
    #     # 0
    #     self.assertEqual(feed.getPosts(0), [])
    #
    #     # Greater than total number of cases
    #     self.assertEqual(feed.getPosts(3), list(feed.posts.all().order_by('-pubDate')))
    #
    #     # Check posts equal
    #     self.assertEqual(feed.getPosts(1), feed.posts.all()[0])
    #
    #     # Empty feed
    #     feed = Feed()
    #     self.assertEqual(feed.getPosts(1), [])


    # def test_get_all(self):
    #     """ Test battery for getAll() """
    #     feed = self.rssFeed
    #
    #     # Test that the default test returns all its posts
    #     self.assertEqual(feed.getAll(), list(feed.posts.all()))
    #
    #     # Test that it returns an empty list with an empty feed
    #     feed = Feed()
    #     self.assertEqual(feed.getAll(), [])

    def test_get_size(self):
        """ Test battery for getSize() """
        # feed = self.rssFeed
        pass

        # # Test the actual feed size return
        # self.assertEqual(feed.getSize(), 1)
        #
        # # Test 0 case
        # feed = Feed()
        # self.assertEqual(feed.getSize(), 0)
        #
        # feed.delete()

class CreateQueueFeedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'bozo8')
        self.topic = Topic.objects.create(name = 'Comics')
        self.topic.save()
        self.f1 = Feed.createByURL("http://xkcd.com/rss.xml")
        self.postNum = 2
        self.interval = '2 days'

    def tearDown(self):
        self.f1.delete()
        self.topic.delete()

    def test_create_queue(self):
        """Creates Queue with correct number of posts, correct posts, correct interval and postNum"""
        #make feed
        q = QueueFeed.create(self.f1, self.postNum, self.interval, self.topic, self.user)

        #test postNum, interval, feed, name
        self.assertEqual(q.postNum, self.postNum)
        self.assertEqual(q.interval, datetime.timedelta(days = 2))
        self.assertEqual(q.feed, self.f1)
        self.assertEqual(q.topic, self.topic)
        self.assertEqual(q.name, "Queue:"+self.f1.title)

        #test qPosts
        fPosts = self.f1.posts.all().order_by('pubDate')
        self.assertItemsEqual(q.queuedPosts.all(), [fPosts[0], fPosts[1]])

        q.delete()

    def test_long_postNum(self):
        """Should return as many posts as possible if postNum is larger than Feed Postlist length"""
        #postNum 5 greater than size of Feed postlist
        pNum = len(self.f1.posts.all()) + 5

        #make QueueFeed with pNum as postNum
        q = QueueFeed.create(self.f1, pNum, self.interval, self.topic, self.user)

        #check accuracy of postNum, interval, feed
        self.assertEqual(q.postNum, pNum)
        self.assertEqual(q.interval, datetime.timedelta(days = 2))
        self.assertEqual(q.feed, self.f1)
        self.assertEqual(q.topic, self.topic)
        self.assertEqual(q.name, "Queue:"+self.f1.title)

        #check that qPosts contains all posts in Feed
        fPosts = self.f1.posts.all().order_by('pubDate')
        self.assertItemsEqual(q.queuedPosts.all(), fPosts)

        q.delete()

class QueueFeedTestCase(TestCase):
    def setUp(self):

        # mock timezone
        # from http://nedbatchelder.com/blog/201209/mocking_datetimetoday.html
        field = User._meta.get_field('timezone')
        mock_now = lambda: datetime.datetime(2014, 12, 1, 21, 32, 54, 706329, tzinfo=pytz.UTC)
        with patch.object(field, 'now', new=mock_now):

            # Create User
            self.user = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'bozo8')
            self.user.save()

            # Create Topic
            self.t1 = self.user.topics.create(name = "Comics")
            self.t1.save()

            # Create Feeds
            self.f1 = Feed.createByURL("http://broodhollow.chainsawsuit.com/feed/")
            self.f1.save()
            self.f1Posts = self.f1.posts.all().order_by('pubDate')

            self.f2 = Feed.createByURL("http://www.last-halloween.com/posts.rss")
            self.f2.save()
            self.f2Posts = self.f2.posts.all().order_by('pubDate')

            # Create QueueFeeds
            self.q1PostNum = 3
            self.q1Interval = '1 hour'
            self.q1 = QueueFeed.create(self.f1, self.q1PostNum, self.q1Interval, self.t1, self.user)

            self.q2PostNum = 2
            self.q2Interval = '2 hours'
            self.q2 = QueueFeed.create(self.f2, self.q2PostNum, self.q2Interval, self.t1, self.user)

            # To test, let's set lastUpdated to an hour ago
            self.q1.lastUpdate = timezone.now() - datetime.timedelta(hours=1, minutes=1)

        def tearDown(self):
            # Since QueueFeed owns the ForeignKey for User, deleting the User deletes its QueueFeeds
            self.user.delete()

            self.f1.delete()
            self.f2.delete()
            self.t1.delete()

            def test_update(self):
                """update should update the qPosts and lastUpdate accurately"""
                self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:3])
                #import pdb; pdb.set_trace()
                self.q1.update()
                self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:6])
                self.assertEqual(self.q1.lastUpdate, timezone.now())

            def test_less_than_interval_update(self):
                """update should not change qPosts or lastUpdate if the Interval hasn't passed"""
                prevUpdate = self.q1.lastUpdate
                self.assertItemsEqual(self.q2.queuedPosts.all(), self.f2Posts[:2])
                self.q1.update()
                self.assertItemsEqual(self.q2.queuedPosts.all(), self.f2Posts[:2])
                self.assertEqual(self.q1.lastUpdate, prevUpdate)

class StaticQueueFeedTestCase(TestCase):

    def setUp(self):
        field = User._meta.get_field('timezone')
        mock_now = lambda: datetime.datetime(2014, 12, 1, 21, 32, 54, 706329, tzinfo=pytz.UTC)
        with patch.object(field, 'now', new=mock_now):

            #create User
            self.user = User.objects.create_user('Devon', 'BAMF@uchicago.edu', 'bozo8')
            self.user.save()

            #add QueueFeed to User's Topic
            self.t1 = self.user.topics.create(name = "Horror")
            self.t1.save()

            #create Feed
            self.f1 = Feed.createByURL("http://broodhollow.chainsawsuit.com/feed/")
            self.f1.save()
            self.f1Posts = self.f1.posts.all().order_by('pubDate')

            #create QueueFeed
            self.q1PostNum = 3
            self.q1Interval = '1 hour'
            self.q1 = QueueFeed.create(self.f1, self.q1PostNum, self.q1Interval, self.t1, self.user)

            #in the interest of testing, set lastUpdated to an hour ago
            self.q1.lastUpdate = timezone.now() - datetime.timedelta(hours = 1)

            #A QueueFeed is always created with static = False; only after creation can a user toggle the static attribute
            self.q1.static = True

            #init a list of posts that have been read for the User
            self.postRead = PostsRead(user = self.user, feed = self.q1.feed)
            self.postRead.save()

    def tearDown(self):
        # since QueueFeed owns the ForeignKey for User, deleting the User deletes its QueueFeeds
        self.user.delete()
        self.f1.delete()
        self.t1.delete()
        self.postRead.delete()

        def test_empty_update(self):
            """if none of the q1PostNum posts have been read and the time interval has passed, qPosts is not refilled"""
            prevUpdate = self.q1.lastUpdate
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:self.q1PostNum])
            self.q1.update()
            # print self.q1.queuedPosts.all()
            # print self.f1Posts[:self.q1PostNum]
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:self.q1PostNum])
            #self.assertEqual(self.q1.lastUpdate, prevUpdate)

        def test_full_update(self):
            """ If all available Posts have been read and the time interval has passed, queuedPosts is refilled """
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:self.q1PostNum])
            #tell postRead that every Post in qPost has been read
            for post in self.q1.queuedPosts.all():
                self.postRead.posts.add(post)
            # print "postRead.posts.all()"
            # print self.postRead.posts.all()
            self.q1.update()
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:(2*self.q1PostNum)])
            #self.assertEqual(self.q1.lastUpdate, timezone.now())

        def test_semi_update(self):
            """ If some of the Posts have been read, queuedPosts is refilled so there are PostNum unread Posts """
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:(self.q1PostNum)])

            #There are three items in qPosts upon init of QueueFeed; user reads one item in qPosts
            self.postRead.posts.add(self.q1.queuedPosts.all()[1])

            self.q1.update()
            #qPosts grows by 1 post instead of 3; the number of unread qPosts is maintained at postNum (3)
            # print self.q1.queuedPosts.all()
            # print self.f1Posts[:self.q1PostNum+1]
            self.assertItemsEqual(self.q1.queuedPosts.all(), self.f1Posts[:self.q1PostNum+1])
            #self.assertEqual(self.q1.lastUpdate, timezone.now())

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
