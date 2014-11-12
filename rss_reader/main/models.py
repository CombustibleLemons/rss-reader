# Django
from django.db import models, IntegrityError
from django.contrib.auth.models import User, UserManager

# RSS Parsing
import feedparser
import time
from datetime import datetime

# Grabbed from http://stackoverflow.com/questions/5216162/how-to-create-list-field-in-django
import ast
import traceback #prints errors

# do we still need this ?
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

        if res["version"] == "rss20":
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
                Post.createByEntry(entry, url, ret_feed)

        return ret_feed

    # Methods
    def getPosts(self, n):
        #empty list, or n is 0
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

        if res["version"] == "rss20":
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
                    Post.createByEntry(entry, self.URL, self)
                except IntegrityError as e:
                    pass # It's okay, an integrity error means we found a duplicate which we've already accounted for.

class Topic(models.Model):
    name = models.TextField(unique=True)
    feeds = models.ManyToManyField(Feed, related_name = '+')
    user = models.ForeignKey(User, null=True, related_name="topics")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        unique_together = (("name","user"),)

    # - editTopicName(name : string)
    def editTopicName(self, topicname):
            self.name = topicname
            self.save()

# - deleteTopic(topic : topic)
# --- already exists as Topic.delete(), ManytoMany relationship means the feeds are dissociated, but not deleted

# - addFeed (feed : Feed)
# - will take advantage of ManytoMany relationships
# - must check that Feed is not already owned in Topic or in User
    def addFeed(self, feed):
        for t in self.user.topics.all():
            if self.feeds.all().filter(URL=feed.URL).exists():
                break
            else:
                if t.feeds.filter(URL = feed.URL).exists():
                    raise FeedExistsInTopic
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

    @classmethod
    def createByEntry(cls, entry, feedURL, feed):
        # Required information for this constructor
        post_dict = {"feed" : feed, "feedURL" : feedURL}

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

        # Create object
        return Post.objects.create(**post_dict)
