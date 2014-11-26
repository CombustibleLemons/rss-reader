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
import traceback #prints errors

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

class UserSettings(models.Model):

    def __unicode__(self):
        return self.readtime

    user = models.OneToOneField(User, primary_key=True, related_name = "settings")

    readtime = models.IntegerField(default = 300) #words per minute

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
    URL = models.URLField(unique=True)

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

class QueueFeed(Feed):
    #QueueFeeds, unlike other Feeds, are unique to a User
    user = models.ForeignKey(User, null=True, related_name="queues")
    feed = models.ForeignKey(Feed, null=True, related_name = "feed")

    #update data
    postNum = models.IntegerField()
    interval = timedelta.fields.TimedeltaField()
    lastUpdate = models.DateTimeField()

    #posts accessible to user
    qPosts = list()
    #static attribute - if static is True, the number of unread posts will not exceed postNum
    static = False

    def create(self, feed, postnum, interval):
        # interval constraints - at smallest, will be hours
        if not(feed.pk):
            feed.save()

        q = QueueFeed()

        q.feed = feed
        posts = feed.posts.all().order_by('pubDate')
        #print posts
        q.qPosts = posts[:postnum]
        #print q.qPosts

        q.postNum = postnum
        q.interval = interval
        q.lastUpdate = timezone.now()
        return q

    def getPosts(self):
        #returns list of posts that should be added to qPosts

        user = self.user
        qfeed = self.feed
        qPosts = self.qPosts

        #calculate timePassed, convert interval from timedelta to hours
        timePassed = (datetime.datetime.now() - self.lastUpdate).total_seconds() / 3600
        print "time passed is %d" % (timePassed,)
        currInt = self.interval.total_seconds() / 3600
        print "interval is %d" % (currInt,)

        #no posts added if not enough time has passed
        if (timePassed<=currInt):
            return list()

        #interval time has passed

        #get entire list of available posts
        ascending_posts = qfeed.posts.all().order_by('pubDate')

        #length of list of current qPosts; how far along Feed's Postlist the QueueFeed has gone
        qPostsLen = len(self.qPosts)

        if (self.static):
            #return list of postNum posts after last Post grabbed
            return list(ascending_posts[qPostsLen:(qPostsLen+self.postNum)])
        else:
            #get number of unread posts in qPosts
            unreadNum = len(qPosts.exclude(id__in=user.readPosts.posts.all()))
            #determine number of Posts that need to be added so that there are postNum unread Posts
            diff = self.postNum - unreadNum
            truncPostNum = diff if (diff < 0) else 0
            return list(ascending_posts[qPostsLen:(qPostsLen+truncPostNum)])

    def update(self):
        with transaction.atomic():
            self.feed.update()
        self.qPosts = qPosts.extend(self.getPosts())

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

    # - deleteTopic(topic : topic)
    # --- already exists as Topic.delete(), ManytoMany relationship means the feeds are dissociated, but not deleted

    # - addFeed (feed : Feed)
    # - will take advantage of ManytoMany relationships
    # - must check that Feed is not already owned in Topic or in User
    def addFeed(self, feed):
        # Remember to exclude self from the checking!
        for t in self.user.topics.all().exclude(id=self.id):
            # Check if the feed is in any other topic
            if t.feeds.filter(id=feed.id).exists():
                raise FeedExistsInTopic
        # Check if feed is in this Topic's feed list
        if self.feeds.all().filter(id=feed.id).exists():
            # Fail to add silently, it's okay if a feed is already in a topic and we add it
            return
        self.feeds.add(feed)
        self.save()

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

        # Text fields (nulls are always empty strings to Django)
        post_dict.update({
            "author" : entry.get("author", ""),
            "rights" : entry.get("rights", ""),
            "title" : entry.get("title", ""),
            "subtitle" : entry.get("subtitle", ""),
            "content" : entry.get("summary", ""),
            "generator" : entry.get("generator", ""),
            "guid" : entry.get("id", ""),
            "url" : entry.get("link", ""),
            "contributor" : entry.get("contributor", "") # TODO: Find a feed where this is enabled
        })

        # Dates
        if entry.get("published_parsed", None):
            pubTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry["published_parsed"])
            #pubTime = entry["published_parsed"]
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
    # Enclosures can be a list, see: https://pythonhosted.org/feedparser/reference-entry-enclosures.html#reference-entry-enclosures-href

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
        for tag in entry.get("tags", []):
            enclosures.append(tag["term"])
        post_dict.update({"enclosure" : enclosures})

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
    posts = models.ManyToManyField(Post, related_name="+", blank=True)
    feed = models.ForeignKey(Feed, related_name="+")
    user = models.ForeignKey(User, related_name="readPosts")
    # Date after which to auto mark as read (TODO: Need a way to handle users marking something as unread
    # and then not just obliterating it everytime this update function is called)
    # dateCutoff defaults to null = True since we do not require posts to be auto-marked-as-read
    dateCutoff = timedelta.fields.TimedeltaField(null=True)

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

# Create 'Uncategorized' Topic to put stuff in on user creation
@receiver(post_save, sender=User)
def createUncategorized(sender, instance, **kwargs):
    try:
        instance.topics.get(name="Uncategorized")
    except Topic.DoesNotExist:
        uncat = Topic(name="Uncategorized", user=instance)
        uncat.save()
    try:
        instance.settings
    except:
        settings = UserSettings(user = instance)
        settings.save()
# Register classes that we want to be able to search
# We will only be returning information about the Feed.
# from https://github.com/etianen/django-watson/wiki/registering-models
watson.register(Feed)
watson.register(Topic)
watson.register(Post)
#watson.register(Post.objects.all(), fields = ("title", "subtitle", "author", "content",))

from django.db.models.signals import post_save
def update_post_index(instance, **kwargs):
    for post in instance.posts.all():
        watson.default_search_engine.update_obj_index(post)

post_save.connect(update_post_index, Feed)
