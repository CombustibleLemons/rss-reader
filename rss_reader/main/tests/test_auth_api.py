# REST Framework
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

# User class from django
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.hashers import make_password

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

class AuthTests(APITestCase):
    @classmethod
    def setUpClass(self):
        self.user = User.objects.create_user(username="shakespeare", password= make_password("shakespeare"))
        self.user.save()
        self.u_id = self.user.id
        self.u_uncat_id = self.user.topics.get(name="Uncategorized").id

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_user_without_login(self):
        """Trying to get the user without login creds should fail"""
        url = '/user/'
        response = self.client.get(url, {}, format = 'json')
        self.assertEqual(response.status_code, 401)

    def test_get_topics_without_login(self):
        """Trying to get topics without login creds should fail"""
        url = '/topics/'
        response = self.client.get(url, {}, format = 'json')
        self.assertEqual(response.status_code, 401)

    def test_create_topic_without_login(self):
        """Trying to create a topic without login creds should fail"""
        url = '/topics/'
        response = self.client.post(url, {"name":"testTopic"}, format = 'json')
        self.assertEqual(response.status_code, 401)

    def test_delete_topic_without_login(self):
        """Trying to delete a topic without login creds should fail"""
        self.client.post('/accounts/login/', {'username':'shakespeare', 'password':'shakespeare'})
        response = self.client.delete('/topics/%d' % (self.u_uncat_id, ), format = 'json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.delete(url, {"name":"testTopic"}, format = 'json')
        self.assertEqual(response.status_code, 401)

    def test_get_user(self):
        """Trying to get the user with login creds should pass"""

        response = self.client.post('/accounts/login/', {'username':'shakespeare', 'password':'shakespeare'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/user/')
        #print "TEST GET USER"
        #print response.data
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_get_topics(self):
        """Trying to get topics with login creds should pass"""
        url = '/topics/'
        response = self.client.post('/accounts/login/', {'username':'shakespeare', 'password':'shakespeare'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, {}, format = 'json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_topic(self):
        """Trying to create a topic with login creds should pass"""
        url = '/topics/'
        response = self.client.post('/accounts/login/', {'username':'shakespeare', 'password':'shakespeare'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {"name":"testTopic"}, format = 'json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_topic(self):
        """Trying to delete a topic with login creds should pass"""
        url = '/topics/'
        response = self.client.post('/accounts/login/', {'username':'shakespeare', 'password':'shakespeare'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, {"name":"testTopic"}, format = 'json')

        if response.status_code == 404:
            response = self.client.post(url, {"name":"testTopic"}, format = 'json')
            self.assertEqual(response.status_code, 200)

        response = self.client.delete(url, {"name":"testTopic"}, format = 'json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
