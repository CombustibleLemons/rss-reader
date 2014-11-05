from rest_framework import generics, permissions

from .serializers import FeedSerializer, PostSerializer, TopicSerializer
from .models import Feed, Post, Topic

class TopicList(generics.ListCreateAPIView):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    # We can limit the fields that we display here so that it is comprehensible to the user.

class TopicDetail(generics.RetrieveAPIView):
    model = Topic
    serializer_class = TopicSerializer

class TopicFeedList(generics.ListAPIView):
    model = Feed
    serializer_class = FeedSerializer
    def get_queryset(self):
        Topic_id = self.kwargs.get("pk")
        queryset = super(TopicFeedList, self).get_queryset()
        return queryset.filter(Topic__pk=Topic_id)


class FeedList(generics.ListCreateAPIView):
    model = Feed
    serializer_class = FeedSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    # We can limit the fields that we display here so that it is comprehensible to the user.

class FeedDetail(generics.RetrieveAPIView):
    model = Feed
    serializer_class = FeedSerializer

class FeedPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    def get_queryset(self):
        feed_id = self.kwargs.get("pk")
        queryset = super(FeedPostList, self).get_queryset()
        return queryset.filter(feed__pk=feed_id)

class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]
