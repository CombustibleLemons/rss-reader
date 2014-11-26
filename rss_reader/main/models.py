# Django

## Models
from django.db import models
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

# User class exists in Django, with email, username attributes; and
# User.objects.create_user(...),check_password(raw pwd),login(),logout(), authenticate() methods
# user.topics.create(name="topicname")

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

    # - deleteTopic(topic : topic)
    # --- already exists as Topic.delete(), ManytoMany relationship means the feeds are dissociated, but not deleted

    # - addFeed (feed : Feed)
    # - will take advantage of ManytoMany relationships
    # - must check that Feed is not already owned in Topic or in User
    # def get_feeds(self):
    #     # import pdb; pdb.set_trace()
    #     return self._feeds.all()
    #
    # def set_feeds(self, feed):
    #     # import pdb; pdb.set_trace()
    #     # Remember to exclude self from the checking!
    #     for t in self.user.topics.all().exclude(id=self.id):
    #         # Check if the feed is in any other topic
    #         if t.feeds.filter(id=feed.id).exists():
    #             raise FeedExistsInTopic
    #     # Check if feed is in this Topic's feed list
    #     if self._feeds.all().filter(id=feed.id).exists():
    #         # Fail to add silently, it's okay if a feed is already in a topic and we add it
    #         return
    #     self._feeds.add(feed)
    #     self.save()
    # feeds = property(get_feeds, set_feeds)

    # - deleteFeed (feed : Feed)
    # - will take advantage of ManytoMany relationship (feed will dissociate)
    def deleteFeed(self, feed):
            self.feeds.remove(feed)
            self.save()

# Enforces validation of feeds that are to be added
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
# TODO: This workaround using Django signals will still add feeds that are correct if we are adding
# multiple feeds at once. We don't do this in the controller code, but that behavior is not
# well defined elsewhere
def topicFeedsChanged(sender, instance, **kwargs):
    # Remember to exclude self from the checking!
    if kwargs['action'] == 'pre_add':
        # We have to keep track of a failed set, since just throwing a ValidationError would cause
        # the Topic objects to lose all of its feeds.
        failed = []
        pk_set = kwargs.get("pk_set").copy()
        for pk in kwargs.get("pk_set"):
            for t in instance.user.topics.all().exclude(id=instance.id):
                # Check if the feed is in any other topic
                if t.feeds.filter(id=pk).exists():
                    # Add the pk to failed list and remove it from the pk_set
                    pk_set.remove(pk)
                    failed.append(pk)
            # Check if feed is in this Topic's feed list
            if instance.feeds.all().filter(id=pk).exists():
                # Fail to add silently, it's okay if a feed is already in a topic and we add it
                pass
        kwargs["pk_set"] = pk_set
        # Since we are forced to use Django signals, put the data into the object and remove it later
        instance.failed = failed
    elif kwargs['action'] == 'post_add':
        # Make sure each added feed is given a PostsRead object to associate with a User
        user = instance.user
        for pk in kwargs["pk_set"]:
            try:
                feed = Feed.objects.get(id=pk)
                pr = PostsRead(user=user, feed=feed)
                pr.save()
            except IntegrityError:
                # IntegrityError means one already exists, so pass
                pass

        # Report any failed pks. See TODO above.
        failed = instance.failed
        if failed:
            errMsg = "Feeds %s already exists in another topic" % (str(failed),)
            failed = []
            raise ValidationError(errMsg)
        # Cleanup the failed rider, don't want it sticking around with the object forever
        del instance.failed

m2m_changed.connect(topicFeedsChanged, sender=Topic.feeds.through)

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
    dateCutoff = timedelta.fields.TimedeltaField(null=True, blank=True) # Blank so serializer doesn't have to keep track

    class Meta:
        unique_together = (('user', 'feed'),);

    @classmethod
    def create(cls, user, feedID, posts):
        cls.user = user
        cls.feed = Feed.objects.get(id=feedID)
        cls.save()
        cls.posts = posts
        return cls

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
watson.register(Topic)
watson.register(Feed)
watson.register(Post)
