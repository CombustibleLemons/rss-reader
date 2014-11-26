from rest_framework import serializers
from .models import User, Topic, Feed, Post, UserSettings, PostsRead

class UserSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    settings = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'topics', 'readPosts' )

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ('readtime',)

class TopicSerializer(serializers.ModelSerializer):
    #feeds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Topic
        #fields = ('id', 'name', 'user', 'feeds', )

class FeedSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Feed
        fields = ("id", "author", "category", "contributor", "description", "docURL",
            "editorAddr", "generator", "guid", "language", "logo", "rights",
            "subtitle", "title", "webmaster", "URL", "ttl", "skipDays",
            "skipHours", "pubDate", "updated", "posts", )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ("feedURL", "author", "category", "rights", "title",
        #     "subtitle", "content", "generator", "guid", "url", "contributor",
        #     "pubDate", "updated", "ackDate", )

class PostsReadSerializer(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = PostsRead
        #fields = ('id', 'user', 'feed', 'posts' )
