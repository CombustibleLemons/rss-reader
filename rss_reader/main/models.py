# Django

## Models
from django.db import models, transaction
from django.contrib.auth.models import User, UserManager
import watson

## Exceptions
from django.db import IntegrityError

## Signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Forms
from django import forms

# RSS Parsing
import feedparser
import time
from datetime import datetime
from django.utils import timezone
import timedelta
import math

# Grabbed from http://stackoverflow.com/questions/5216162/how-to-create-list-field-in-django
import ast
import traceback # prints errors

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# User class exists in Django, with email, username attributes; and
# User.objects.create_user(...),check_password(raw pwd),login(),logout(), authenticate() methods
# user.topics.create(name="topicname")

class UserSettings(models.Model):

    def __unicode__(self):
        return self.readtime

    user = models.OneToOneField(User, primary_key=True, related_name = "settings")

    readtime = models.IntegerField(default = 300) # words per minute

class FeedURLInvalid(Exception):
    pass

class FeedExistsInTopic(Exception):
    pass

class Feed(models.Model):
    # Attributes

    # Text
    # - author : string
    author = models.TextField()
    # - category : string
    category = models.TextField()
    # - contributor : string
    contributor = models.TextField()
    # - description : string
    description = models.TextField()
    # - docURL : string
    docURL = models.TextField()
    # - editorAddr : string
    editorAddr = models.TextField()
    # - generator : string
    generator = models.TextField()
    # - guid : string
    guid = models.TextField()
    # - language : string
    language = models.TextField()
    # - logo : string
    logo = models.TextField()
    # - rights : string
    rights =  models.TextField()
    # - subtitle : string
    subtitle = models.TextField()
    # - title : string
    title = models.TextField()
    # - webmaster : string
    webmaster = models.TextField()

    # URL
    # - URL : string
    URL = models.TextField(unique=True)

    # Integer
    # - ttl : int
    ttl = models.IntegerField(null=True)
    # - skipDays : int
    skipDays = models.IntegerField(null=True)
    # - skipHours : int
    skipHours = models.IntegerField(null=True)

    # Date
    # - pubDate : date
    pubDate = models.DateTimeField(null=True)
    # - updated : date
    updated = models.DateTimeField(null=True)
    # - logo : (string, string, string)

    def __unicode__(self):
        return self.title

    # Constructor (uses class method as suggested by Django docs)
    @classmethod
    def createByURL(cls, url):
        res = feedparser.parse(url)
        # Check if bozo_exception was raised
        if res["version"] == "":
            raise FeedURLInvalid

        elif res["version"] in [u"rss", u"rss20", u"atom", u"atom10"]:
            # Populate Feed fields
            feedData = res["feed"]

            # docURL can sometimes by hidden in the links
            docURL = feedData.get("link", "")
            if docURL == "":
                try:
                    for link in feedData["links"]:
                        if link["rel"] == "self":
                            docURL = link["href"]
                except KeyError:
                    docURL = "";

            # Text fields
            cls_dict = {
                "author" : feedData.get("author", ""),
                "category" : feedData.get("category", ""),
                "contributor" : feedData.get("contributor", ""),
                "description" : feedData.get("description", ""),
                "docURL" : docURL,
                "editorAddr" : feedData.get("editorAddr", ""),
                "generator" : feedData.get("generator", ""),
                "guid" : feedData.get("guid", ""),
                "language" : feedData.get("language", ""),
                "rights" : feedData.get("rights", ""),
                "title" : feedData.get("title", ""),
                "subtitle" : feedData.get("subtitle", ""),
            }
            if feedData.get("image",None):
                cls_dict.update({"logo" : feedData["image"].get("href", "")})
            else:
                cls_dict.update({"logo" : ""})

            # Integer field
            cls_dict.update({
                "ttl" : int(feedData["ttl"]) if feedData.get("ttl", None) else None,
                "skipDays" : int(feedData["skipDays"]) if feedData.get("skipDays", None) else None,
                "skipHours" : int(feedData["skipHours"]) if feedData.get("skipHours", None) else None
            })

            # Date fields
            if feedData.get("published_parsed", None):
                pubTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', feedData["published_parsed"])
                cls_dict.update({"pubDate" : pubTime})

            if res.get("updated_parsed", None):
                updateTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', res["updated_parsed"])
                cls_dict.update({"updated" : updateTime})

            # URL Field
            try:
                clsURL = url
                # next(x["href"] for x in feedData["links"] if x["rel"] == "self")
            except StopIteration:
                clsURL = ""
            if url:
                cls_dict.update({"URL" : clsURL})

            ret_feed = cls.objects.create(**cls_dict)

            # Create Posts
            for entry in res["entries"]:
                if res["version"] in ["rss", "rss20"]:
                    RSS.createByEntry(entry, url, ret_feed)
                elif res["version"] in ["atom", "atom10"]:
                    Atom.createByEntry(entry, url, ret_feed)

        return ret_feed

    # Methods
    def getPosts(self, n):
        # Empty list, or n is 0
        if (not(self.posts.all().exists()) or (n==0)):
            return list(self.posts.none())

        descending_posts = self.posts.all().order_by('-pubDate')
        if (n==1):
            return self.posts.all()[0]
        return list(descending_posts[:(n-1)])

    def getAll(self):
        return list(self.posts.all())

    def getSize(self):
        return self.posts.all().count()

    def update(self):
        res = feedparser.parse(self.URL)
        # Check if bozo_exception was raised
        if res["version"] == "":
            raise FeedURLInvalid

        # Supported versions
        elif res["version"] in [u"rss20", u"atom10"]:
            # Populate Feed fields
            feedData = res["feed"]

            # Text fields
            cls_dict = {
                "author" : feedData.get("author", ""),
                "category" : feedData.get("category", ""),
                "contributor" : feedData.get("contributor", ""),
                "description" : feedData.get("description", ""),
                "docURL" : feedData.get("docURL", ""),
                "editorAddr" : feedData.get("editorAddr", ""),
                "generator" : feedData.get("generator", ""),
                "guid" : feedData.get("guid", ""),
                "language" : feedData.get("language", ""),
                "rights" : feedData.get("rights", ""),
                "title" : feedData.get("title", ""),
                "subtitle" : feedData.get("subtitle", ""),
            }
            if feedData.get("image",None):
                cls_dict.update({"logo" : feedData["image"].get("href", "")})
            else:
                cls_dict.update({"logo" : ""})

            # Integer field
            cls_dict.update({
                "ttl" : int(feedData["ttl"]) if feedData.get("ttl", None) else None,
                "skipDays" : int(feedData["skipDays"]) if feedData.get("skipDays", None) else None,
                "skipHours" : int(feedData["skipHours"]) if feedData.get("skipHours", None) else None
            })

            # Date fields
            if feedData.get("published_parsed", None):
                pubTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', feedData["published_parsed"])
                cls_dict.update({"pubDate" : pubTime})

            if res.get("updated_parsed", None):
                updateTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', res["updated_parsed"])
                cls_dict.update({"updated" : updateTime})

            self.__dict__.update(cls_dict)

            # Create Posts
            for entry in res["entries"]:
                try:
                    if res["version"] == "rss20":
                        RSS.createByEntry(entry, self.URL, self)
                    elif res["version"] == "atom10":
                        Atom.createByEntry(entry, self.URL, self)
                except IntegrityError as e:
                    # We've found a duplicate, but its fine if we've found a duplicate
                    pass

class Topic(models.Model):
    name = models.TextField()
    feeds = models.ManyToManyField(Feed, related_name = '+')
    user = models.ForeignKey(User, null=True, related_name="topics")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        unique_together = (("name","user"),)

    # - editTopicName(name : string)
    def editTopicName(self, topicname):
        tmp = self.name
        try:
            self.name = topicname
            self.save()
        except IntegrityError as e:
            self.name = tmp
            raise e

    # - deleteFeed (feed : Feed)
    # - will take advantage of ManytoMany relationship (feed will dissociate)
    def deleteFeed(self, feed):
        self.feeds.remove(feed)
        self.save()

class Post(models.Model):
    # Attributes
    # Text
    # - feedURL : string (comes from the Feed class)
    feedURL = models.TextField()
    # - author : string
    author = models.TextField()
    # - category : string [*]
    category = ListField()
    # - rights : string
    rights = models.TextField()
    # - title : string
    title = models.TextField()
    # - subtitle : string
    subtitle = models.TextField()
    # - content : string
    content = models.TextField()
    # - generator : string
    generator = models.TextField()
    # - guid : string
    guid = models.TextField()
    # - url : string
    url = models.TextField()
    # - contributor : string
    contributor = models.TextField()

    # Date
    # - pubDate : date
    pubDate = models.DateTimeField(null=True)
    # - updated : date
    updated = models.DateTimeField(null=True)

    # Internal system acknowledgement date
    # - ackDate : float
    ackDate = models.FloatField(null=True)

    # Foreign Keys (i.e. other models)
    # Feed that post belongs to
    feed = models.ForeignKey(Feed, related_name="posts")

    # Since new posts will not (if the feed is correctly formed) have duplicate guids
    class Meta:
        unique_together = (('feed', 'guid'),);

    # Methods
    def __unicode__(self):
        return self.title

    @staticmethod
    def generateClassDict(entry):
        post_dict = dict()

        # Categories is a set of tags for feedparser
        categories = list()
        for tag in entry.get("tags", []):
            categories.append(tag["term"])
        post_dict.update({"category" : categories})

        # Content can sometimes be in the summary or in the content field
        content = entry.get("content", "")
        if content == "":
            content = entry.get("summary", "")
        else:
            content = content[0]["value"]

        # Text fields (nulls are always empty strings to Django)
        post_dict.update({
            "author" : entry.get("author", ""),
            "rights" : entry.get("rights", ""),
            "title" : entry.get("title", ""),
            "subtitle" : entry.get("subtitle", ""),
            "content" : content,
            "generator" : entry.get("generator", ""),
            "guid" : entry.get("id", ""),
            "url" : entry.get("link", ""),
            "contributor" : entry.get("contributor", "") # TODO: Find a feed where this is enabled
        })

        # Dates
        if entry.get("published_parsed", None):
            pubTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry["published_parsed"])
            # pubTime = entry["published_parsed"]
            post_dict.update({"pubDate" : pubTime})

        if entry.get("updated_parsed", None):
            updateTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry["updated_parsed"])
            post_dict.update({"updated" : updateTime})

        # AckDate (DateTime that the post enters the database)
        post_dict.update({"ackDate" : time.time()})

        return post_dict

    @classmethod
    def createByEntry(cls, entry, feedURL, feed):
        pass # Virtual constructor


class RSS(Post):
    # Comments are a URL to a comments page
    comments = models.URLField()
    enclosure = ListField()
    # Enclosures can be a list, see: https://pythonhosted.org/feedparser/reference-entry-enclosures.html# reference-entry-enclosures-href

    @classmethod
    def createByEntry(cls, entry, feedURL, feed):
        # Required information for this constructor
        post_dict = {"feed" : feed, "feedURL" : feedURL}
        post_dict.update(cls.generateClassDict(entry))

        # Special attributes for RSS
        # Comments
        post_dict.update({"comments" : entry.get("comments", "")})

        # Enclosures
        enclosures = list()
        try:
            for link in entry.get("links", []):
                if link["rel"] == "enclosure":
                    enclosures.append(link["href"])
            post_dict.update({"enclosure" : enclosures})
        except KeyError:
            pass
        # TODO: Functionality for tags
        # for tag in entry.get("tags", []):
        # enclosures.append(tag["term"])

        # Create object
        return RSS.objects.create(**post_dict)

class Atom(Post):
    # Comments are a URL to a comments page
    summary = models.TextField()

    @classmethod
    def createByEntry(cls, entry, feedURL, feed):
        # Required information for this constructor
        post_dict = {"feed" : feed, "feedURL" : feedURL}
        post_dict.update(cls.generateClassDict(entry))

        # Special attributes for RSS
        # Comments
        post_dict.update({"summary" : entry.get("summary", "")})

        # Create object
        atom = Atom.objects.create(**post_dict)

        # Save before we exit
        atom.save()
        return atom

import timedelta
import datetime
import pytz
class PostsRead(models.Model):
    # Model Attributes
    posts = models.ManyToManyField(Post, null=True, related_name="+readPosts")
    feed = models.ForeignKey(Feed, related_name="+")
    user = models.ForeignKey(User, related_name="readPosts")
    # Date after which to auto mark as read (TODO: Need a way to handle users marking something as unread
    # and then not just obliterating it everytime this update function is called)
    # dateCutoff defaults to null = True since we do not require posts to be auto-marked-as-read
    dateCutoff = timedelta.fields.TimedeltaField(null=False, blank=True) # Blank so serializer doesn't have to keep track

    class Meta:
        unique_together = (('user', 'feed'),);

    def update(self):
        # Auto-update the posts read according to the setting for feed ranges
        if self.dateCutoff:
            now = datetime.datetime.now(pytz.utc)
            for post in self.feed.posts.all():
                if now - self.dateCutoff >= post.pubDate:
                    # Datetime is outside of the acceptable range, remove it from the list.
                    self.posts.add(post)

    def getUnreadPostsByNum(self, n):
        return self.getUnreadPosts()[:n]

    def getUnreadPosts(self):
        feedPosts = self.feed.posts.all()
        if self.posts.all():
            return feedPosts.exclude(id__in=self.posts.all())
        return feedPosts

class QueueFeed(models.Model):
    # QueueFeeds, unlike other Feeds, are unique to a User
    user = models.ForeignKey(User, null=True, related_name="queues")
    feed = models.ForeignKey(Feed, null=True, related_name="feed")
    topic = models.ForeignKey(Topic, null=True, related_name="queue_feeds")
    postsReadInQueue = models.ManyToManyField(Post, null=True, related_name="+QueueFeedReadPosts")

    name = models.TextField()

    # Update data
    postNum = models.IntegerField()
    interval = timedelta.fields.TimedeltaField()
    lastUpdate = models.DateTimeField()

    # List of posts accessible to user, by post.id
    queuedPosts = models.ManyToManyField(Post, null=True, related_name="+")

    # Static attribute - if static is True, the number of unread posts will not exceed postNum
    static = models.BooleanField(default=False)

    @classmethod
    def create(cls, feed, postnum, interval, topic, user):
        """Create a QueueFeed object that makes `postnum` posts available every `interval`"""
        # Interval constraints - at smallest, will be hours.
        # For debugging and tests, we may set it lower
        # Initialize a QueueFeed
        queue = cls.objects.create(postNum=postnum, interval=interval, lastUpdate=timezone.now(), topic=topic, user=user, feed=feed, name="Queue:" + feed.title)

        # Fill the queue
        feedPosts = feed.posts.all().order_by('pubDate')
        queue.queuedPosts.add(*(feedPosts[:postnum]))
        return queue

    def getPosts(self):
        """Returns list of Post ids that should be added to queuedPosts"""
        # Alias some of the self variables
        user = self.user
        queueFeed = self.feed
        queuedPosts = self.queuedPosts

        # USE PYTHONS UTILITIES LIKE THEY ARE PYTHON UTILITIES!!
        # Calculate timePassed, convert interval from timedelta to hours
        if timezone.now() < (self.lastUpdate + self.interval):
            return []

        # We are past the time for an update, so update the last update variable
        self.lastUpdate = timezone.now()

        # Get entire list of available posts
        ascendingPosts = queueFeed.posts.all().order_by('pubDate')

        # Length of list of current queuedPosts; how far along Feed's Postlist the QueueFeed has gone
        queuedPostsLen = len(self.queuedPosts.all())

        if not self.static:
            # Return list of postNum posts after last Post grabbed
            return list(ascendingPosts[queuedPostsLen:(queuedPostsLen+self.postNum)])

        # Get queueFeed's read posts from readPosts
        feedReadPost = user.readPosts.get(feed__id=queueFeed.id)
        feedReadPostSet = list(feedReadPost.posts.all())
        # print "feedReadPosts"
        # print feedReadPostSet
        # print "queuedPosts"
        # print queuedPosts.all()

        # Make list of unread posts
        unread = [post for post in queuedPosts.all() if not queueFeed.posts.get(id=post.id) in feedReadPostSet]

        # Determine number of Posts that need to be added so that there are postNum unread Posts
        diff = self.postNum - len(unread)
        truncPostNum = diff if diff > 0 else 0
        return list(ascendingPosts[queuedPostsLen:(queuedPostsLen+truncPostNum)])

    def update(self):
        """Update function to run every interval"""
        for post in self.getPosts():
            self.queuedPosts.add(post)
