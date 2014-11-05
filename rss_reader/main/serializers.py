from rest_framework import serializers
from .models import User, Topic, Feed, Post

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
