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

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback

class UserTests(APITestCase):
    def setUp(self):
        self.user = User(username="shakespeare")
        self.user.save() #user creation isn't tested in iteration 1, it is assumed a user exists.
        self.u_id = self.user.id
        self.model_u = User(username="eecummings")
        self.u = UserSerializer(self.model_u)

    def tearDown(self):
        self.user.delete()

    def test_userlist_exists(self):
        #a userlist can only have 1 user in iteration 1
        """Check that UserList is alive and well"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': self.u_id, 'username': u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': []}])

    def test_username_change(self):
        """Trying to change the username should fail"""
        url = '/users/%d' % (self.u_id,)
        response = self.client.post(url, {'username':u'marlowe'}, format = 'json')
        self.assertEqual(response.status_code, 405)

    def test_userdetail_exists(self):
        """Check that UserDetail is accurate"""
        response = self.client.get('/users/%d' % (self.u_id,))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': self.u_id, 'username':u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': []})

    def test_user_cannot_be_created(self): #there is one user in iteration 1, so a second one cannot be created
        """Iteration 1 should have one user, so users cannot be made"""
        response = self.client.put('/users/', self.u.data, format='json')
        self.assertEqual(response.status_code, 405)

class TopicTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User(username="shakespeare")
        cls.user.save()
        cls.u_id = cls.user.id
        cls.t1_m = Topic(name = "sonnets", user = cls.user)
        cls.t1_id = cls.t1_m.id
        cls.t2_m = Topic(name = "tragedies", user = cls.user)
        cls.t2_id = cls.t2_m.id
        cls.evil_t1_m = Topic(name = "tragedies", user=cls.user)
        cls.evil_t1_id = 154 #shakespeare wrote this many sonnets!
        cls.t1 = TopicSerializer(cls.t1_m)
        cls.t2 = TopicSerializer(cls.t2_m)
        cls.evil_t1 = TopicSerializer(cls.evil_t1_m)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_uncategorized_exists(cls):
        """Uncategorized should be a default Topic"""
        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{u'id':0,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[]}])


    def test_add_topic(cls):
        """Tests that Topic can be added"""
        response = cls.client.put('/topics/', cls.t1.data, format='json')
        cls.assertEqual(response.status_code, 200)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{u'id':0,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[]}, {u'id': cls.t1_id, 'name': u'sonnets', 'user': cls.u_id, 'feeds': []}])

        response = cls.client.put('/topics/', cls.t2.data, format = 'json')
        cls.assertEqual(response.status_code, 200)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{u'id':0,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[]}, {u'id':cls.t1_id, 'name':u'sonnets','user':cls.u_id, 'feeds':[]},{u'id':cls.t2_id, 'name':u'tragedies','user':cls.u_id, 'feeds':[]}])

    def test_add_repeat_topic(cls):
        """Adding a Topic with the same name as an existent Topic will fail"""
        response = cls.client.put('/topics/', cls.evil_t1.data, format='json')
        cls.assertEqual(response.status_code, 405)

    def test_rename_topic(cls):
        """Tests that Topic can be renamed"""
        url = '/topics/%d' % (cls.t2_id,)
        response = cls.client.post(url, {'name':u'comedies'}, format='json')
        assertEqual(response.status_code, 200)
        response = cls.client.get(url)
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, {u'id':cls.t2_id, 'name':u'comedies', 'user':cls.u_id,'feeds':[]})

    def test_rename_repeat_topic(cls):
        """Tests that Topic renamed with another Topic's name fails"""
        url = '/topics/%d' % (cls.t2_id,)
        response = cls.client.post(url, {'name':u'sonnets'}, format='json')
        cls.assertEqual(response.status_code, 405)

    def test_rename_uncategorized(cls):
        """The Uncategorized Topic cannot be renamed"""
        url = '/topics/1'
        reponse = cls.client.post(url,{'name':u'tragedies'}, format='json')
        cls.assertEqual(response.status_code, 200)
        response = cls.client.get(url)
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, {u'id':1, 'name':u'Uncategorized', 'user':cls.u_id,'feeds':[]})

    def test_delete_topic(cls):
        """Tests that Topic can be deleted"""
        response = cls.client.delete('/topics/%d' % (cls.t2_id,))
        cls.assertEqual(response.status_code, 200)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{u'id':0,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[]}, {u'id': cls.t1_id, 'name': u'sonnets', 'user': cls.u_id, 'feeds': []}])

        response = cls.client.delete('/topics/%d' % (cls.t1_id,))
        cls.assertEqual(response.status_code, 200)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{u'id':0,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[]}])

    def test_delete_nonexistent_topic(cls):
        """A Topic that does not exist should fail upon attempted deletion"""
        url = '/topics/%d' % (cls.evil_t1_id,)
        response = cls.client.delete(url)
        cls.assertEqual(response.status_code, 405)


    def test_delete_uncategorized(cls):
        """The Uncategorized Topic cannot be removed"""
        response = cls.client.delete('/topics/0')
        cls.assertEqual(response.status_code, 405)


class FeedTests(APITestCase):
    @classmethod
    def setUpClass(cls):
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

    def test_create_feed(cls):
        """Test that Feed can be created by URL"""
        response = cls.client.put('/feeds/create', cls.f1_url)
        cls.assertEqual(response.status_code, 200)

        response = cls.client.get('/feeds/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [{"id": 1, "name": "Uncategorized", "user": 1, "feeds": [1]}])

        #gets newly created feed object and its id
        cls.f1 = Feed.objects.all()[0]
        cls.f1_id = cls.f1.id

    def test_feed_detail_exists(cls):
        """Test accuracy of feed details"""
        response = cls.client.get('/feeds/%d' % (cls.f1_id, ))
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, cls.f1_details)

    def test_post_list_exists(cls):
        """Test accuracy of post list"""
        response = cls.client.get('/feeds/%d/posts' % (cls.f1_id, ))
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, cls.f1_post_list)

    def test_delete_feed(cls):
        """Test feed deletion"""
        response = cls.client.delete('/feed/%d' % (cls.f1_id,))
        cls.assertEqual(response.status_code, 200)
        response = cls.client.get('/feeds/')
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [])

class PostTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.f1 = Feed.createByURL("http://home.uchicago.edu/~jharriman/example-rss.xml")
        cls.f1.save()
        cls.f1_id = cls.f1.id
        cls.p1_id = cls.f1.posts.all()[0].id
        cls.p1_data = {
            {u'id': cls.p1_id,
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
            'feed': cls.f1_id}}

    @classmethod
    def tearDownClass(cls):
        cls.f1.delete()

    def test_post_detail_exists(cls):
        """Test accuracy of post"""
        response = cls.client.get('/posts/%d' % (cls.p1_id, ))
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, cls.p1_data)
