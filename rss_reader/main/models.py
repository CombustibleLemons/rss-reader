# Django
from django.db import models
from django.db.models.signals import post_init

# RSS Parsing
import feedparser
import time
from datetime import datetime

# Grabbed from http://stackoverflow.com/questions/5216162/how-to-create-list-field-in-django
import ast

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

class Feed(models.Model):
    # Attributes
    # - URL : string
    URL = models.URLField(unique=True)
    # - logo : (string, string, string)
    # - title : string
    title = models.TextField()
    # - subtitle : string
    subtitle = models.TextField()
    # - description : string
    description = models.TextField()
    # - language : string
    language = models.TextField()
    # - rights : string
    rights =  models.TextField()
    # - editorAddr : string
    editorAddr = models.TextField()
    # - webmaster : string
    webmaster = models.TextField()
    # - pubDate : date
    pubDate = models.TextField()
    # - category : string
    category = models.TextField()
    # - generator : string
    generator = models.TextField()
    # - docURL : string
    docURL = models.TextField()
    # - ttl : int
    ttl = models.IntegerField(null=True)
    # - logo : string
    logo = models.TextField()
    # - skipDays : int
    skipDays = models.IntegerField(null=True)
    # - skipHours : int
    skipHours = models.IntegerField(null=True)
    # - author : string
    author = models.TextField()
    # - contributor : string
    contributor = models.TextField()
    # - guid : string
    guid = models.TextField()
    # - updated : date
    updated = models.DateTimeField(null=True)

    # Constructor (uses class method as suggested by Django docs)
    @classmethod
    def createByUrl(cls, url):
        res = feedparser.parse(url)
        # Check if bozo_exception was raised
        if res.get("bozo_exception", None):
            pass
            # TODO: Raise invalid URL exception

        if res["version"] == "rss20":
            # Populate Feed fields
            feedData = res["feed"]
            cls_dict = {"language" : feedData["language"],
                        "title" : feedData["title"],
                        "subtitle" : feedData["subtitle"],
                        "updated" : time.strftime('%Y-%m-%dT%H:%M:%SZ', res["updated_parsed"]),
                        "URL" : url
            }
            ret_feed = cls.objects.create(**cls_dict)

            # Create Posts
            for entry in res["entries"]:
                Post.createByEntry(entry, url, ret_feed)
                
        return ret_feed
# from main.models import *
# f = Feed.createByUrl("http://xkcd.com/rss.xml")

    # Methods
    def getPosts(self, n):
        pass

    def getAll(self):
        print self.post_set.all()

    def getSize(self):
        pass

class Post(models.Model):
    # Attributes
    # - ackDate : int
    ackData = models.IntegerField(null=True)
    # - author : string
    author = models.TextField()
    # - category : string [*]
    category = ListField()
    # - feedURL : string
    feedURL = models.TextField()
    # - rights : string
    rights = models.TextField()
    # - subtitle : string
    subtitle = models.TextField()
    # - content : string
    content = models.TextField()
    # - generator : string
    generator = models.TextField()
    # - guid : string
    guid = models.TextField()
    # - title : string
    title = models.TextField()
    # - url : string
    url = models.TextField()
    # - pubDate : date
    pubDate = models.DateTimeField(null=True)
    # - contributor : string
    contributor = models.TextField()
    # - updated : date
    updated = models.DateTimeField(null=True)

    # Feed that post belongs to
    feed = models.ForeignKey(Feed)

    # Methods
    @classmethod
    def createByEntry(cls, entry, feedURL, feed):
        # Required information for this constructor
        post_dict = {"feed" : feed, "feedURL" : feedURL}

        # Text fields (nulls are always empty strings)
        post_dict.update({
            "guid" : entry.get("id", ""),
            "content" : entry.get("summary", ""),
            "title" : entry.get("title", ""),
            "subtitle" : entry.get("subtitle", "")

        })

        # Dates
        pubTime = entry.get("published_parsed", None)
        if pubTime:
            post_dict.update({
                "pubDate" : time.strftime('%Y-%m-%dT%H:%M:%SZ', pubTime)
            })

        p = Post.objects.create(**post_dict)
