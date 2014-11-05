from rest_framework import serializers
from .models import Feed, Post

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
