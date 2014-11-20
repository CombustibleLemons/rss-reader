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
from main.serializers import UserSerializer, TopicSerializer, FeedSerializer, PostSerializer, UserSettingsSerializer
from main.models import Topic, Feed, Post, UserSettings
from django.forms.models import model_to_dict

## Transaction Management
from django.db import transaction

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback
from django.contrib.auth import authenticate

class LoggedOutUserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="fitzgerald", password = "ruto")
        self.user.save()

        self.t1 = Topic(name = "novels", user = self.user)
        self.t1.save()
        self.user.topics.add(self.t1)

        self.t2 = Topic(name = "short stories", user = self.user)
        self.t2.save()
        self.t2_data = model_to_dict(self.t2)

        self.f1 = Feed.createByURL("http://xkcd.com/rss.xml")
        self.f1.save()

        self.f2_url = "http://home.uchicago.edu/~jharriman/example-rss.xml"

    def tearDown(self):
        self.t1.delete()
        self.t2.delete()
        self.user.delete()
        self.f1.delete()

    def test_add_topic(self):
        """Adding a Topic should fail when User is not logged in"""
        response = self.client.post('/topics/create', self.t2_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_rename_topic(self):
        """Renaming a Topic should fail when User is not logged in"""
        response = response = self.client.patch(('/topics/%d' % (self.t1.id,)), {'name':u'novellas'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_topic(self):
        """Deleting a Topic should fail when User is not logged in"""
        response = self.client.post("/topics/delete", {"index" : self.t1.id})
        self.assertEqual(response.status_code, 401)

    def test_create_feed(self):
        """Creating a Feed should not fail - we want to improve our database :) """
        #does not add to any User Topic's list of Feeds
        response = self.client.post('/feeds/create', {"url" : self.f2_url})
        self.assertEqual(response.status_code, 200)

    def test_delete_feed(self):
        """Deleting a Feed should fail when User is not logged in"""
        response = self.client.delete("/feeds/%d" % (self.f1.id,))
        self.assertEqual(response.status_code, 200)


class UserTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="shakespeare", password="anne")
        cls.user.save()
        cls.u_id = cls.user.id
        cls.u_uncat_id = cls.user.topics.get(name="Uncategorized").id
        cls.model_u = User(username="eecummings")
        cls.u = UserSerializer(cls.model_u)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        # Log the client in as the User
        self.client.login(username="shakespeare", password="anne")

    def tearDown(self):
        self.client.logout()

    def test_username_change(self):
        """Trying to change the username should fail"""
        url = '/user/'
        response = self.client.post(url, {'username':u'marlowe'}, format = 'json')
        self.assertEqual(response.status_code, 405)

    def test_userdetail_exists(self):
        """Check that UserDetail is accurate"""
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': self.u_id, 'username':u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': [self.u_uncat_id]})

    def test_uncategorized_exists(self):
        """Uncategorized should be a default Topic for a newly created User"""
        response = self.client.get('/topics/')
        self.assertEqual(response.status_code, 200)
        self.assertItemsEqual(response.data, [{u'id':self.u_uncat_id,'name':u'Uncategorized', 'user':self.u_id, 'feeds':[]}])

    def test_settings_exist(self):
        """Users should be created with settings"""
        response = self.client.get('/user/settings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'readtime':300})

    def test_settings_update(self):
        """readtimes in UserSettings can be changed"""
        response = self.client.patch('/user/settings/', {'readtime':'400'})
        self.assertEqual(response.status_code,200)

        response = self.client.get('/user/settings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'readtime': 400})

    # Old tests that are no longer needed
    # We no longer have a userlist model
    # def test_userlist_exists(self):
    #     # A userlist can only have 1 user in iteration 1
    #     """Check that UserList is alive and well"""
    #     response = self.client.get('/users/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, [{'id': self.u_id, 'username': u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': [self.u_uncat_id]}])

    # This is iteration 2, we can remove this
    # def test_user_cannot_be_created(self): #there is one user in iteration 1, so a second one cannot be created
    #     """Iteration 1 should have one user, so users cannot be made"""
    #     response = self.client.put('/users/', self.u.data, format='json')
    #     self.assertEqual(response.status_code, 405)
