from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RSSUserSerializer, TopicSerializer, FeedSerializer, PostSerializer
from .models import RSSUser, Topic, Feed, Post

# RSSUser API
class RSSUserList(generics.ListCreateAPIView):
    model = RSSUser
    serializer_class = RSSUserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class RSSUserDetail(generics.RetrieveAPIView):
    model = RSSUser
    serializer_class = RSSUserSerializer

class RSSUserTopicList(generics.ListAPIView):
    model = Topic
    serializer_class = TopicSerializer
    def get_queryset(self):
        RSSUser_id = self.kwargs.get("pk")
        queryset = super(RSSUserFeedList, self).get_queryset()
        return queryset.filter(RSSUser__pk=RSSUser_id)

# Topic API
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

# Feed API
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

@api_view(['GET','POST'])
def feed_create(request):
    if request.method == "POST":
        # Create feed using input URL
        print request.DATA["url"]
        return Response(status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Post API
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
