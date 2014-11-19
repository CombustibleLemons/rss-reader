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

class UserTests(APITestCase):
    def setUp(self):
        self.user = User(username="shakespeare")
        self.user.save() #user creation isn't tested in iteration 1, it is assumed a user exists.
        self.u_id = self.user.id
        self.u_uncat_id = self.user.topics.get(name="Uncategorized").id
        self.model_u = User(username="eecummings")
        self.u = UserSerializer(self.model_u)

    def tearDown(self):
        self.user.delete()

    def test_userlist_exists(self):
        #a userlist can only have 1 user in iteration 1
        """Check that UserList is alive and well"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': self.u_id, 'username': u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': [self.u_uncat_id]}])

    def test_username_change(self):
        """Trying to change the username should fail"""
        url = '/users/%d' % (self.u_id,)
        response = self.client.post(url, {'username':u'marlowe'}, format = 'json')
        self.assertEqual(response.status_code, 405)

    def test_userdetail_exists(self):
        """Check that UserDetail is accurate"""
        response = self.client.get('/users/%d' % (self.u_id,))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': self.u_id, 'username':u'shakespeare', 'first_name': u'', 'last_name': u'', 'topics': [self.u_uncat_id]})

    def test_user_cannot_be_created(self): #there is one user in iteration 1, so a second one cannot be created
        """Iteration 1 should have one user, so users cannot be made"""
        response = self.client.put('/users/', self.u.data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_uncategorized_exists(self):
        """Uncategorized should be a default Topic for a newly created User"""
        response = self.client.get('/topics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{u'id':self.u_uncat_id,'name':u'Uncategorized', 'user':self.u_id, 'feeds':[]}])