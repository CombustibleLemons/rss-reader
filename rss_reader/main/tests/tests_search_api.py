# REST Framework
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

# User class from django
from django.contrib.auth.models import User, UserManager
from django.core.management import call_command

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

#import watson
import watson
from watson.registration import RegistrationError, get_backend, SearchEngine
from watson.models import SearchEntry

class SearchTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        call_command("installwatson", verbosity=0)
        cls.registered_models = watson.get_registered_models()
        # Remove all the current registered models.
        for model in cls.registered_models:
            watson.unregister(model)
        # Register the test models.
        watson.register(Feed)
        watson.register(Post)
        watson.register(Topic)

        # init user
        cls.user = User.objects.create_user(username = "Lucia", email = "pokey@penguin.com", password = "cumberbumberwumbers")
        cls.user.save()

        #init videogame Feeds
        Feed.createByURL("http://penny-arcade.com/feed").save()
        Feed.createByURL("http://thepunchlineismachismo.com/feed").save()
        Feed.createByURL("http://rss.escapistmagazine.com/articles/comicsandcosplay/comics/critical-miss.xml").save()
        Feed.createByURL("http://xkcd.com/rss.xml").save()
        Feed.createByURL("http://rss.nytimes.com/services/xml/rss/nyt/Golf.xml").save()

        cls.f1_m = Feed.objects.get(URL = "http://penny-arcade.com/feed")
        cls.f1 = FeedSerializer(cls.f1_m).data

        cls.f2_m = Feed.objects.get(URL = "http://thepunchlineismachismo.com/feed")
        cls.f2 = FeedSerializer(cls.f2_m).data

        cls.f3_m = Feed.objects.get(URL = "http://rss.escapistmagazine.com/articles/comicsandcosplay/comics/critical-miss.xml")
        cls.f3 = FeedSerializer(cls.f3_m).data

        cls.f4_m = Feed.objects.get(URL = "http://xkcd.com/rss.xml")
        cls.f4 = FeedSerializer(cls.f4_m).data

        cls.f5_m = Feed.objects.get(URL = "http://rss.nytimes.com/services/xml/rss/nyt/Golf.xml")
        cls.f5 = FeedSerializer(cls.f5_m).data

    @classmethod
    def tearDownClass(cls):
        #Unregister test models.
        watson.unregister(Feed)
        watson.unregister(Post)
        watson.unregister(Topic)
        # Re-register the old registered models.
        for model in cls.registered_models:
            watson.register(model)
        # Unregister the test models.
        cls.user.delete()
        cls.f1_m.delete()
        cls.f2_m.delete()
        cls.f3_m.delete()
        cls.f4_m.delete()

    def setUp(self):
        # Log the client in as the User
        self.client.login(username="Lucia", password="cumberbumberwumbers")

    def tearDown(self):
        self.client.logout()

    def test_search_feeds(cls):
        """Confirms that search covers Feed titles"""
        #f1, f2, and f3 titles contain words "Penny" and "Critical"
        #Tests that search works with half of word, different capitalization
        response = cls.client.post("/search/", {"searchString":"Penn cRITical"})
        cls.assertEqual(response.status_code, 200)
        cls.assertTrue(cls.f1 in response.data)
        cls.assertTrue(cls.f3 in response.data)

    def test_search_feeds_and_topics(cls):
        """Topics exist - the search should search Topics and Feeds, and return a list of Feeds"""
        #init "videogames" Topic, with f1 and f2
        webcomics = Topic(name = "webcomics", user = cls.user)
        webcomics.save()

        # Add NYT's Golf RSS to webcomics
        webcomics.feeds.add(cls.f5_m)

        #Topic and f2 and f4 fields both contain word "webcomic"
        #NYT, by virtue of being under "webcomic" is returned
        response = cls.client.post("/search/", {"searchString":"webcomic"})
        cls.assertEqual(response.status_code, 200)
        #cls.assertItemsEqual(response.data, [cls.f3, cls.f4, cls.f5])
        cls.assertTrue(cls.f3 in response.data)
        cls.assertTrue(cls.f4 in response.data)
        cls.assertTrue(cls.f5 in response.data)

    def test_search_posts(cls):
        """Search covers post content"""
        #"game" occurs in Post content for f1 and f2, in Feed and Post content for f3
        response = cls.client.post("/search/", {"searchString" : "game"})
        cls.assertEqual(response.status_code, 200)
        #print response.data
        #cls.assertItemsEqual(response.data, [cls.f1, cls.f2, cls.f3])
        #cls.assertTrue(cls.f1 in response.data)
        cls.assertTrue(cls.f2 in response.data)
        cls.assertTrue(cls.f3 in response.data)

        #Penny Arcade discusses "Gabe" in *multiple* Posts; multiple Posts returned from one Feed still returns one Feed result
        response = cls.client.post("/search/", {"searchString" : "Gabe"})
        cls.assertEqual(response.status_code, 200)
        #cls.assertItemsEqual(response.data, [cls.f1])
        cls.assertTrue(cls.f1 in response.data)

    def test_users_discarded(cls):
        """Should discard user results"""
        user2 = User(username = "webcomic")
        user2.save()

        response = cls.client.post("/search/", {"searchString":"webcomic"})
        cls.assertEqual(response.status_code, 200)
        #cls.assertItemsEqual(response.data, [cls.f3, cls.f4])
        cls.assertTrue(cls.f3 in response.data)
        cls.assertTrue(cls.f4 in response.data)

    def test_empty_return_list(cls):
        """Should return an empty list"""
        response = cls.client.post("/search/", {"searchString":"ethics"})
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.data, [])

    def test_unrecognized_url(cls):
        """Should return list of Feeds given an approximate url starting with http"""
        response = cls.client.post("/search/", {"searchString":"http://xkcd.com/rss."})
        cls.assertEqual(response.status_code, 200)
        #cls.assertItemsEqual(response.data, [cls.f5, cls.f4, cls.f3])
        cls.assertTrue(cls.f3 in response.data)
        cls.assertTrue(cls.f4 in response.data)
        cls.assertTrue(cls.f5 in response.data)

        response = cls.client.post("/search/", {"searchString": "http://penny-arcade.com/"})
        cls.assertEqual(response.status_code, 200)
        #cls.assertEqual(response.data, [cls.f1])
        cls.assertTrue(cls.f1 in response.data)

        # response = cls.client.post("/search/", {"searchString":"http://journalism.com"})
        # cls.assertEqual(response.data, [cls.f3])
