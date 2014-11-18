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

def FeedSearchTests(APITestCase):
    @classmethod
    def setUpClass(cls):

        # init user
        cls.user = User(username = "Lucia")
        cls.user.save()

        #init videogame Feeds
        cls.f1 = Feed.createByURL("http://penny-arcade.com/feed")
        cls.f1.save()
        cls.f2 = Feed.createByURL("http://thepunchlineismachismo.com/feed")
        cls.f2.save()
        cls.f3 = Feed.createByURL("http://www.vgcats.com/vgcats.rdf.xml")
        cls.f3.save()

    def tearDownClass(cls):
        cls.user.delete()
        cls.f1.delete()
        cls.f2.delete()
        cls.f3.delete

    def test_search_feeds(cls):
        """No Topics - the search should return a list of Feeds"""
        cls.assertEqual(True, False)
        response = cls.client.get("/search", {"searchString":"video games"})
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, "blugh")

    def test_search_feeds_and_topics(cls):
        """Topics exist - the search should still return a list of Feeds"""
        #init "videogames" Topic, with f1 and f2
        videogames = Topic(name = "videogames", user = cls.user)
        videogames.save()
        videogames.addFeed(cls.f1)
        videogames.addFeed(cls.f2)

        response = cls.client.get("/search", {"searchString":"video games"})
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, "blugh")
