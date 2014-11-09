from rest_framework import serializers
from .models import User, Topic, Feed, Post

class UserSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'topics', )

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic

class FeedSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Feed
        fields = ("author", "category", "contributor", "description", "docURL",
            "editorAddr", "generator", "guid", "language", "logo", "rights",
            "subtitle", "title", "webmaster", "URL", "ttl", "skipDays",
            "skipHours", "pubDate", "updated", "posts", )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ("feedURL", "author", "category", "rights", "title",
        #     "subtitle", "content", "generator", "guid", "url", "contributor",
        #     "pubDate", "updated", "ackDate", )
