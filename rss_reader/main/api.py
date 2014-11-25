# REST Framework
from rest_framework import generics, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# User class from django
from django.contrib.auth.models import User, UserManager

# For overriding response when a User is requested
from django.shortcuts import get_object_or_404

# Models and Serializers
from .serializers import UserSerializer, TopicSerializer, FeedSerializer, PostSerializer, UserSettingsSerializer, PostsReadSerializer
from .models import Topic, Feed, Post, UserSettings, PostsRead

from pprint import pprint

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

    def get_object(self):
        queryset = self.get_queryset()
        # Force username to be from the requesting user
        filter = {"username" : self.request.user}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class UserSettingsDetail(generics.RetrieveUpdateAPIView):
    model = UserSettings
    serializer_class = UserSettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        # Force username to be from the requesting user
        filter = {"user" : User.objects.get(username = self.request.user)}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class UserTopicList(generics.ListAPIView):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        User_id = self.kwargs.get("pk")
        queryset = super(UserTopicList, self).get_queryset()
        return queryset.filter(User__pk=User_id)

# Topic API
class TopicList(generics.ListCreateAPIView):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # Filter out Topics from other users that are not the requester
    def create(self, request, *args, **kwargs):
        try:
            # Add the user to the data
            user = User.objects.get(username=request.user)
            data = request.DATA
            data.update({"user" : user.id})
            serializer = self.get_serializer(data=data, files=request.FILES)

            if serializer.is_valid():
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            # Return 409 if the url already exist
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print e
            # Return bad request if we get a general exception
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        print self.request.user
        userID = User.objects.get(username=self.request.user)
        queryset = super(TopicList, self).get_queryset()
        return queryset.filter(user=userID)

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if topic name is uncategorized, if so we can't delete it
        if instance.name == "Uncategorized":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()
        # Check to make sure this is not an uncategorized Topic
        if self.object.name == "Uncategorized" and request.DATA["name"] != "Uncategorized":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self.object, data=request.DATA,
                                        files=request.FILES, partial=partial)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            # full_clean on model instance may be called in pre_save,
            # so we have to handle eventual errors.
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)
        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopicFeedList(generics.ListAPIView):
    model = Feed
    serializer_class = FeedSerializer
    permission_classes = (permissions.IsAuthenticated,)
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

class FeedDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Feed
    serializer_class = FeedSerializer

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

# TODO: These functions are deprecated and will be removed as soon as the rest of the system does not require them
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
@api_view(['GET', 'POST'])
def search(request):
    if request.method == "POST":
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

# Posts read are never destroyed, users will always have access to this data.
class PostsReadDetail(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    model = PostsRead
    serializer_class = PostsReadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        # Add the user to the data
        user = User.objects.get(username=request.user)
        feedId = self.kwargs.get("pk")
        data = request.DATA
        data.update({"user" : user.id})
        data.update({"feed" : feedId})
        serializer = self.get_serializer(data=data, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        feed_id = self.kwargs.get("pk")
        queryset = super(PostsReadDetail, self).get_queryset()
        return queryset.filter(feed__pk=feed_id)


# Get unread posts
@api_view(['GET'])
def unread_posts(request, **kwargs):
    if request.method == "GET":
        # Create feed using input URL
        feedID = kwargs.pop("pk")
        try:
            user = User.objects.get(username=request.user)
            readPostObj = user.readPosts.get(feed=feedID)
            unreadPosts = readPostObj.getUnreadPosts()
            serialized_list = [PostSerializer(x).data for x in unreadPosts]
            return Response(serialized_list, status=status.HTTP_200_OK)
        except Exception as e:
            # Return bad request if we get a general exception
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
