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

class TopicAddTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        # Create User
        cls.user = User.objects.create_user(username="shakespeare", password="anne")
        cls.user.save()
        cls.u_id = cls.user.id

        # Grab Uncategorized Topic
        cls.user_uncat = cls.user.topics.get(name="Uncategorized")

        # Create other topics
        cls.t1_m = Topic(name = "sonnets", user = cls.user)
        cls.t2_m = Topic(name = "tragedies", user = cls.user)
        cls.evil_t1_m = Topic(name = "tragedies", user=cls.user)

        # Turn topics into JSON objects
        cls.t1_data = model_to_dict(cls.t1_m)
        cls.t2_data = model_to_dict(cls.t2_m)
        cls.evil_t1_data = model_to_dict(cls.evil_t1_m)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(username="shakespeare", password="anne")

    def tearDown(self):
        self.client.logout()

    def test_add_topic(cls):
        """Tests that Topic can be added"""
        response = cls.client.post('/topics/', cls.t1_data, format='json')
        cls.assertEqual(response.status_code, 201)
        t1Server = Topic.objects.get(name=cls.t1_data["name"])
        t1_id = t1Server.id

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        # We don't care about the order the server returns things in
        cls.assertItemsEqual(response.data, [{u'id':cls.user_uncat.id,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[], 'queue_feeds': []},
                                            {u'id': t1_id, 'name': u'sonnets', 'user': cls.u_id, 'feeds': [], 'queue_feeds' : []}])

        response = cls.client.post('/topics/', cls.t2_data, format = 'json')
        cls.assertEqual(response.status_code, 201)
        t2Server = Topic.objects.get(name=cls.t2_data["name"])
        t2_id = t2Server.id

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        # We don't care about the order the server returns things in
        cls.assertItemsEqual(response.data, [{u'id':cls.user_uncat.id,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[], 'queue_feeds': []},
                                            {u'id':t1_id, 'name':u'sonnets','user':cls.u_id, 'feeds':[], 'queue_feeds': []},
                                            {u'id':t2_id, 'name':u'tragedies','user':cls.u_id, 'feeds':[], 'queue_feeds': []}])
        # Cleanup topics on server
        t1Server.delete()
        t2Server.delete()

    def test_add_repeat_topic(cls):
        """Adding a Topic with the same name as an existent Topic will fail"""
        cls.t2_m.save()
        with transaction.atomic():
            response = cls.client.post('/topics/', cls.evil_t1_data, format='json')
        cls.assertEqual(response.status_code, 409)
        cls.t2_m.delete()

class TopicTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        # Create User
        cls.user = User.objects.create_user(username="shakespeare", password="anne")
        cls.user.save()
        cls.u_id = cls.user.id

        # Grab Uncategorized Topic
        cls.user_uncat = cls.user.topics.get(name="Uncategorized")

        # Create other topics
        cls.t1_m = Topic(name = "sonnets", user = cls.user)
        cls.t1_m.save()
        cls.t1_id = cls.t1_m.id

        cls.t2_m = Topic(name = "tragedies", user = cls.user)
        cls.t2_m.save()
        cls.t2_id = cls.t2_m.id

        cls.evil_t1_m = Topic(name = "tragedies", user=cls.user)
        cls.evil_t1_id = 154 # shakespeare wrote this many sonnets! <- Be more subtle Lucia, let the reader figure it out

        # Turn topics into JSON objects
        cls.evil_t1_data = model_to_dict(cls.evil_t1_m)

    @classmethod
    def tearDownClass(cls):
        cls.t1_m.delete()
        cls.t2_m.delete()
        cls.user.delete()

    def setUp(self):
        self.client.login(username="shakespeare", password="anne")

    def tearDown(self):
        self.client.logout()

    def test_rename_topic(cls):
        """Tests that Topic can be renamed"""
        url = "/topics/%d" % (cls.t2_id,)
        #print cls.t2_m
        cls.t2_m.name = "comedies"
        # print cls.t2_m
        # print "Serializing"
        # t = TopicSerializer(cls.t2_m)
        # print "Serialized"
        response = cls.client.put(url, TopicSerializer(cls.t2_m).data, format='json')
        cls.assertEqual(response.status_code, 200)
        response = cls.client.get(url)
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, {u'id':cls.t2_id, 'name':u'comedies', 'user':cls.u_id,'feeds':[], 'queue_feeds': []})

        # Set it back for further tests
        resetTopic = Topic.objects.get(name="comedies")
        resetTopic.name="tragedies"
        resetTopic.save()

    def test_rename_repeat_topic(cls):
        """Tests that Topic renamed with another Topic's name fails"""
        url = '/topics/%d' % (cls.t2_id,)
        cls.t2_m.name = "sonnets"
        response = cls.client.put(url, TopicSerializer(cls.t2_m).data, format='json')
        cls.assertEqual(response.status_code, 400)

    def test_rename_nameless_topic(cls):
        """A Test cannot be renamed without a name"""
        url = '/topics/%d' % (cls.t2_id,)
        cls.t2_m.name = ""
        response = cls.client.patch(url, TopicSerializer(cls.t2_m).data, format='json')
        cls.assertEqual(response.status_code, 400)

    def test_rename_uncategorized(cls):
        """The Uncategorized Topic cannot be renamed"""

        cls.user_uncat.name = "tragedies"
        response = cls.client.put(("/topics/%d" % cls.user_uncat.id), TopicSerializer(cls.user_uncat).data, format='json')
        cls.assertEqual(response.status_code, 400)

        response = cls.client.get("/topics/%d" % cls.user_uncat.id)
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data, {u'id':cls.user_uncat.id, 'name':u'Uncategorized', 'user':cls.u_id,'feeds':[], 'queue_feeds':[]})

    def test_delete_topic(cls):
        """Tests that Topic can be deleted"""
        response = cls.client.delete("/topics/%d" % cls.t2_id)
        cls.assertEqual(response.status_code, 204)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data, [{u'id':cls.user_uncat.id,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[], 'queue_feeds':[]},
                                            {u'id': cls.t1_id, 'name': u'sonnets', 'user': cls.u_id, 'feeds': [], 'queue_feeds':[]} ])

        response = cls.client.delete("/topics/%d" % cls.t1_id)
        cls.assertEqual(response.status_code, 204)

        response = cls.client.get('/topics/')
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data, [{u'id':cls.user_uncat.id,'name':u'Uncategorized', 'user':cls.u_id, 'feeds':[], 'queue_feeds': []}])

    def test_delete_nonexistent_topic(cls):
        """A Topic that does not exist should fail upon attempted deletion"""
        response = cls.client.delete('/topics/%d' % cls.evil_t1_id)
        cls.assertEqual(response.status_code, 404)

    def test_delete_uncategorized(cls):
        """The Uncategorized Topic cannot be removed"""
        response = cls.client.delete('/topics/%d' % cls.user_uncat.id)
        cls.assertEqual(response.status_code, 400)
