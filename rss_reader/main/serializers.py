from rest_framework import serializers
from .models import RSSUser, Topic, Feed, Post

class RSSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
