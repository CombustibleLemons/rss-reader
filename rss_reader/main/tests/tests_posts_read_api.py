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
from main.models import Topic, Feed, Post, PostsRead
from django.forms.models import model_to_dict

## Transaction Management
from django.db import transaction

# Python built-ins required for tests
import time
import datetime
import pytz
import traceback

class PostsReadTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="shakespeare", password="anne")
        cls.user.save()
        cls.f1_url = "http://xkcd.com/rss.xml"
        cls.f1 = Feed.createByURL(cls.f1_url)
        cls.t1 = cls.user.topics.get(name="Uncategorized")
        cls.t1.feeds.add(cls.f1)
                

    @classmethod
    def tearDownClass(cls):
        cls.user.topics.get(name="Uncategorized").delete()
        cls.user.delete()
        cls.f1.delete()
        # Make sure to delete the feed so we don't run into other tests

    def setUp(self):
        self.client.login(username="shakespeare", password="anne")

    def tearDown(self):
        self.client.logout()

    def test_post_detail_exists(cls):
        """Test existence of post details"""
        response = cls.client.get("/feeds/{}/posts/read".format(cls.f1.id))

        cls.assertEqual(response.status_code, 200)

    def test_posts_unread(cls):
        """Test all posts are unread at first i.e. there are no read posts"""
        response = cls.client.get("/feeds/{}/posts/read".format(cls.f1.id))
        cls.assertEqual(response.status_code, 200)
        cls.assertItemsEqual(response.data['posts'], [])

    def test_mark_post_read(cls):
        """Test if post is marked as read"""
        
        prObj = PostsRead.objects.get(feed=cls.f1, user=cls.user)
        oldUnread = len(prObj.getUnreadPosts())

        pst = cls.f1.posts.all()[0]
        prObj.posts.add(pst)
        prObj.save()

        unreadPosts = cls.f1.posts.exclude(id=pst.id) 
        readPosts = [cls.f1.posts.get(id=pst.id)]

        cls.assertItemsEqual(prObj.getUnreadPosts(), unreadPosts)
        cls.assertItemsEqual(readPosts, prObj.posts.all())
        cls.assertEqual(len(prObj.getUnreadPosts())+1, oldUnread)xx