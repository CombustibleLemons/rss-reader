# REST Framework
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

# User class from django
from django.contrib.auth.models import User, UserManager

# Models and Serializers
from main.serializers import UserSerializer, TopicSerializer, FeedSerializer, PostSerializer
from main.models import Topic, Feed, Post
from django.forms.models import model_to_dict

## Transaction Management
from django.db import transaction

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback

class FeedCreateTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="FeedTests")
        cls.user.save()
        cls.f1_url = "http://home.uchicago.edu/~jharriman/example-rss.xml"
        cls.f1_id = None
        cls.f1 = None
        cls.f1_post_list = [
        {
            "id": 6,
            "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "author": "By KATIE HAFNER",
            "category": [],
            "rights": "",
            "title": "Bracing for the Falls of an Aging Nation",
            "subtitle": "",
            "content": "As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif\" width=\"1\" /><br clear=\"all\" />",
            "generator": "",
            "guid": "http://www.nytimes.com/interactive/2014/11/03/health/bracing-for-the-falls-of-an-aging-nation.html",
            "url": "http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
            "contributor": "",
            "pubDate": "2014-11-02T13:43:10Z",
            "updated": "2014-11-02T13:43:10Z",
            "ackDate": 1415855355.56354,
            "feed": 2
            },
        {
            "id": 5,
            "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "author": "By LYNN VAVRECK",
            "category": ["Elections, Senate","United States Politics and Government","Elections, House of Representatives", "Voting and Voters", "Midterm Elections (2014)"],
            "rights": "",
            "title": "Midterm Calculus: The Economy Elects Presidents. Presidents Elect Congress.",
            "subtitle": "",
            "content": "While presidential elections are shaped largely by economic performance, the largest factor in midterm elections is the president.",
            "generator": "",
            "guid": "http://www.nytimes.com/2014/11/03/upshot/the-economy-elects-presidents-presidents-elect-congress.html",
            "url": "http://rss.nytimes.com/c/34625/f/642562/s/40134217/sc/1/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Cthe0Eeconomy0Eelects0Epresidents0Epresidents0Eelect0Econgress0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
            "contributor": "",
            "pubDate": "2014-11-02T14:00:22Z",
            "updated": "2014-11-02T14:00:22Z",
            "ackDate": 1415855355.55587,
            "feed": 2
            }]

        cls.f1_details = {
            "id": cls.f1_id,
            "author": "",
            "category": "",
            "contributor": "",
            "description": "US",
            "docURL": "",
            "editorAddr": "",
            "generator": "",
            "guid": "",
            "language": "en-us",
            "logo": "http://graphics8.nytimes.com/images/misc/NYT_logo_rss_250x40.png",
            "rights": "Copyright 2014 The New York Times Company",
            "subtitle": "US",
            "title": "NYT > U.S.",
            "webmaster": "",
            "URL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "ttl": 5,
            "skipDays": None,
            "skipHours": None,
            "pubDate": "2014-11-02T16:13:02Z",
            "updated": "2014-11-06T01:00:31Z",
            "posts": [2,1]
            }

    @classmethod
    def tearDownClass(cls):
        cls.user.topics.get(name="Uncategorized").delete()
        cls.user.delete()
        # Make sure to delete the feed so we don't run into other tests

    def test_create_feed(cls):
        """Test that Feed can be created by URL"""
        response = cls.client.post('/feeds/create/', {"url" : cls.f1_url})
        cls.assertEqual(response.status_code, 200)

        # response = cls.client.get('/feeds/')
        # cls.assertEqual(response.status_code, 200)
        # cls.assertEqual(response.data, [{'id': 1, 'author': u'', 'category': u'',
        #                                 'contributor': u'', 'description': u'US',
        #                                 'docURL': u'http://www.nytimes.com/pages/national/index.html?partner=rss&ampemc=rss',
        #                                 'editorAddr': u'', 'generator': u'', 'guid': u'',
        #                                 'language': u'en-us',
        #                                 'logo': u'http://graphics8.nytimes.com/images/misc/NYT_logo_rss_250x40.png',
        #                                 'rights': u'Copyright 2014 The New York Times Company',
        #                                 'subtitle': u'US', 'title': u'NYT > U.S.', 'webmaster': u'',
        #                                 'URL': u'http://home.uchicago.edu/~jharriman/example-rss.xml',
        #                                 'ttl': 5, 'skipDays': None, 'skipHours': None,
        #                                 'pubDate': datetime.datetime(2014, 11, 2, 16, 13, 2, tzinfo=pytz.UTC),
        #                                 'updated': datetime.datetime(2014, 11, 6, 1, 0, 31, tzinfo=pytz.UTC),
        #                                 'posts': [2, 1]}])
        #
        # #gets newly created feed object and its id
        # cls.f1 = Feed.objects.get(id=response.data[0]["id"])
        # cls.f1_id = cls.f1.id
        # cls.f1.delete()

class FeedTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="FeedTests")
        cls.user.save()
        cls.f1_url = "http://home.uchicago.edu/~jharriman/example-rss.xml"
        cls.f1_id = None
        cls.f1 = None
        cls.f1_post_list = [
        {
            "feedURL": u"http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "author": u"By KATIE HAFNER",
            "category": [],
            "rights": u"",
            "title": u"Bracing for the Falls of an Aging Nation",
            "subtitle": u"",
            "content": u"As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif\" width=\"1\" /><br clear=\"all\" />",
            "generator": u"",
            "guid": u"http://www.nytimes.com/interactive/2014/11/03/health/bracing-for-the-falls-of-an-aging-nation.html",
            "url": u"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
            "contributor": u"",
            "pubDate": u"2014-11-02T13:43:10Z",
            "updated": u"2014-11-02T13:43:10Z",
            "ackDate": 1415855355.56354,
            "feed": 2
            },
        {
            "feedURL": u"http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "author": u"By LYNN VAVRECK",
            "category": ["Elections, Senate","United States Politics and Government","Elections, House of Representatives", "Voting and Voters", "Midterm Elections (2014)"],
            "rights": u"",
            "title": u"Midterm Calculus: The Economy Elects Presidents. Presidents Elect Congress.",
            "subtitle": u"",
            "content": u"While presidential elections are shaped largely by economic performance, the largest factor in midterm elections is the president.",
            "generator": u"",
            "guid": u"http://www.nytimes.com/2014/11/03/upshot/the-economy-elects-presidents-presidents-elect-congress.html",
            "url": u"http://rss.nytimes.com/c/34625/f/642562/s/40134217/sc/1/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Cthe0Eeconomy0Eelects0Epresidents0Epresidents0Eelect0Econgress0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
            "contributor": u"",
            "pubDate": u"2014-11-02T14:00:22Z",
            "updated": u"2014-11-02T14:00:22Z",
            "ackDate": 1415855355.55587,
            "feed": 2
            }]

        cls.f1 = Feed.createByURL(cls.f1_url)
        cls.p1 = Post.objects.get(guid="http://www.nytimes.com/interactive/2014/11/03/health/bracing-for-the-falls-of-an-aging-nation.html")
        cls.p2 = Post.objects.get(guid="http://www.nytimes.com/2014/11/03/upshot/the-economy-elects-presidents-presidents-elect-congress.html")
        cls.f1_details = {
            "id": cls.f1_id,
            "author": u"",
            "category": u"",
            "contributor": u"",
            "description": u"US",
            "docURL": u"",
            "editorAddr": u"",
            "generator": u"",
            "guid": u"",
            "language": u"en-us",
            "logo": u"http://graphics8.nytimes.com/images/misc/NYT_logo_rss_250x40.png",
            "rights": u"Copyright 2014 The New York Times Company",
            "subtitle": u"US",
            "title": u"NYT > U.S.",
            "webmaster": u"",
            "URL": u"http://www.nytimes.com/services/xml/rss/nyt/US.xml",
            "ttl": 5,
            "skipDays": None,
            "skipHours": None,
            "pubDate" : datetime.datetime(2014, 11, 2, 16, 13, 2, tzinfo=pytz.UTC),
            "updated": datetime.datetime(2014, 11, 6, 1, 0, 31, tzinfo=pytz.UTC),
            "posts": [cls.p1.id,cls.p2.id]
        }
        cls.f1_id = cls.f1.id

    @classmethod
    def tearDownClass(cls):
        cls.user.topics.get(name="Uncategorized").delete()
        cls.user.delete()
        cls.f1.delete()
        # Make sure to delete the feed so we don't run into other tests

    def test_feed_detail_exists(cls):
        """Test accuracy of feed details"""
        response = cls.client.get("/feeds/%d" % (cls.f1_id, ))
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data, cls.f1_details)

    def test_post_list_exists(cls):
        """Test accuracy of post list"""
        response = cls.client.get("/feeds/%d/posts/" % (cls.f1_id, ))
        cls.assertEqual(response.status_code, 200)
        # Delete the ids, since they are added by the server and not really relevant to checking correctness
        for post in response.data:
            del post["id"]
        for res, exp in response.data, cls.f1_post_list:
            cls.assertItemsEqual(res, exp)

    def test_delete_feed(cls):
        """Test feed deletion"""
        response = cls.client.delete("/feeds/%d" % (cls.f1_id,))
        cls.assertEqual(response.status_code, 204)

        # no list of all feeds
        # response = cls.client.get("/feeds/")
        # cls.assertEqual(response.status_code, 200)
        # cls.assertEqual(response.data, [])

class PostTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.f1 = Feed.createByURL("http://home.uchicago.edu/~jharriman/example-rss.xml")
        cls.f1.save()
        cls.f1_id = cls.f1.id
        cls.p1_id = cls.f1.posts.all()[0].id
        cls.p1_data = {
            u'id': cls.p1_id,
            'feedURL': u'http://www.nytimes.com/services/xml/rss/nyt/US.xml',
            'author': u'By KATIE HAFNER',
            'category': [],
            'rights': u'',
            'title': u'Bracing for the Falls of an Aging Nation',
            'subtitle': u'',
            'content': u'As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border="0" height="1" src="http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif" width="1" /><br clear="all" />',
            'generator': u'',
            'guid': u'http://www.nytimes.com/interactive/2014/11/03/health/bracing-for-the-falls-of-an-aging-nation.html',
            'url': u'http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm',
            'contributor': u'',
            'pubDate': datetime.datetime(2014, 11, 2, 13, 43, 10, tzinfo=pytz.UTC),
            'updated': datetime.datetime(2014, 11, 2, 13, 43, 10, tzinfo=pytz.UTC),
            'ackDate': 1415858199.31228,
            'feed': cls.f1_id
        }

    @classmethod
    def tearDownClass(cls):
        cls.f1.delete()

    def test_post_detail_exists(cls):
        """Test accuracy of post"""
        response = cls.client.get('/posts/%d' % (cls.p1_id, ))
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data, cls.p1_data)
