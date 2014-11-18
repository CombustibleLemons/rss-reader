# REST Framework
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# User class from django
from django.contrib.auth.models import User, UserManager

# Models and Serializers
from .serializers import UserSerializer, TopicSerializer, FeedSerializer, PostSerializer
from .models import Topic, Feed, Post

# User API
class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class UserDetail(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        print request.user
        return self.retrieve(request, *args, **kwargs)

class UserTopicList(generics.ListAPIView):
    model = Topic
    serializer_class = TopicSerializer
    def get_queryset(self):
        User_id = self.kwargs.get("pk")
        queryset = super(UserTopicList, self).get_queryset()
        return queryset.filter(User__pk=User_id)

# Topic API
class TopicList(generics.ListCreateAPIView):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data=request.DATA, files=request.FILES)
       if serializer.is_valid():
           self.pre_save(serializer.object)
           self.object = serializer.save(force_insert=True)
           self.post_save(self.object, created=True)
           headers = self.get_success_headers(serializer.data)
           return Response(serializer.data, status=status.HTTP_201_CREATED,
                           headers=headers)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
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

class FeedDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Feed
    serializer_class = FeedSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class FeedPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    def get_queryset(self):
        feed_id = self.kwargs.get("pk")
        queryset = super(FeedPostList, self).get_queryset()
        return queryset.filter(feed__pk=feed_id)

from django.db import IntegrityError
@api_view(['GET','POST'])
def feed_create(request):
    if request.method == "POST":
        # Create feed using input URL
        url = request.DATA["url"]
        try:
            # Try creating a Feed with the url
            f = Feed.createByURL(url)
            f.save()

            # Add feed to uncategorized Topic
            user = User.objects.all()[0] # TODO: Change this so that individual users can be recognized
            try:
                # If uncategorized already exists
                t = user.topics.get(name="Uncategorized")
            except Topic.DoesNotExist as e:
                # If it doesn't create it
                t = Topic(name="Uncategorized", user=user)
                t.save()

            # Add the Feed to the Topic
            t.addFeed(f)
            t.save()

            # Serialize the Feed so it can be sent back
            fs = FeedSerializer(f)
            return Response(fs.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            # Check if user already subscribed, then we have a genuine error
            user = User.objects.get(id="1")
            existsInOtherTopic = False
            for topic in user.topics.all():
                if topic.feeds.filter(URL=url).exists():
                    existsInOtherTopic = True
                    break
            if not existsInOtherTopic:
                # Find the feed
                f = Feed.objects.get(URL=url)
                try:
                    # If uncategorized already exists
                    t = user.topics.get(name="Uncategorized")
                except Topic.DoesNotExist as e:
                    # If it doesn't create it
                    t = Topic(name="Uncategorized", user=user)
                    t.save()
                t.addFeed(f)
                fs = FeedSerializer(f)
                return Response(fs.data, status=status.HTTP_200_OK)
            # User is already subscribed to feed elsewhere,
            # Return 409 CONFLICT
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print e
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['POST'])
def topic_create(request):
    if request.method == "POST":
        # Create topic using input name
        topicName = request.DATA.get("name")
        try:
            user = User.objects.all()[0] # TODO: Change this so that individual users can be recognized

            # Try creating a Topic with the name
            t = Topic(name=topicName, user=user)
            t.save()

            # Serialize the Topic so it can be sent back
            ts = TopicSerializer(t)
            return Response(ts.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Return 409 if the url already exist
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print e
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def topic_delete(request):
    if request.method == "POST":
        # Delete topic using input name

        topicID = request.DATA.get("index")
        try:
            user = User.objects.all()[0] # TODO: Change this so that individual users can be recognized

            # Try deleting a topic
            t = Topic.objects.get(id=topicID, user=user)

            # Can't delete the Uncategorized topic from the user
            if t.name == "Uncategorized":
                return Response(status=status.HTTP_400_BAD_REQUEST)
            t.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
            # Return 409 if the url already exist
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def topic_rename(request):
    if request.method == "POST":
        # Rename topic using input name

        topicID = request.DATA.get("index")
        try:
            user = User.objects.all()[0] # TODO: Change this so that individual users can be recognized

            # Try deleting a topic
            t = Topic.objects.get(id=topicID, user=user)
            if t.name == "Uncategorized":
                return Response(status=status.HTTP_400_BAD_REQUEST)
            t.name = request.DATA.get("name", t.name)
            t.save()

            # Serialize the Topic so it can be sent back
            ts = TopicSerializer(t)
            return Response(ts.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            # Return 409 if the url already exist
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print e
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Search
import watson
@api_view(['GET'])
def search(request):
    if request.method == "GET":
        # Create feed using input URL
        searchString = request.DATA.get("searchString")
        try:
            results = watson.search(searchString)
            # Results can contain Feeds, Topics, Posts, you name it
            # Get at the feed for each post and then uniq the data
            feeds = list()
            # TODO Pare this list down before parsing for objects
            for result in results:
                obj = result.object
                if type(obj) == Topic:
                    topicFeeds = map(lambda x: FeedSerializer(x).data, obj.feeds)
                    feeds.extend(topicFeeds)
                elif type(obj) == Post:
                    fs = FeedSerializer(obj.feed)
                    feeds.append(fs.data)
                elif type(obj) == Feed:
                    fs = FeedSerializer(obj)
                    feeds.append(fs.data)
                else:
                    # We do nothing if the search object is a User
                    pass
            # TODO: Verify feed relevancy is in the right order
            return Response(feeds, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)
