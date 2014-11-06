from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FeedSerializer, PostSerializer, TopicSerializer
from .models import Feed, Post, Topic
# class FeedList(APIView):
#     """
#     List all feeds, or create a new feed.
#     """
#     def get(self, request, format=None):
#         feeds = Feed.objects.all()
#         serializer = FeedSerializer(feeds, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = FeedSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class FeedDetail(APIView):
#     """
#     Retrieve, update or delete a Feed instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Feed.objects.get(pk=pk)
#         except Feed.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         feed = self.get_object(pk)
#         serializer = FeedSerializer(feed)
#         return Response(serializer.data)
#
#     def post(self, request, pk, format=None):
#         # Check DATA for url and create a feed from url
#         url = request.DATA["url"]
#         serializer = FeedSerializer(feed, data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         feed = self.get_object(pk)
#         feed.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

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

@api_view(['GET','POST'])
def feed_create(request):
    if request.method == "POST":
        # Create feed using input URL
        print request.DATA["url"]
        return Response(status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
