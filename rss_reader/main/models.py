from django.db import models

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

class Post(models.Model):
    # - ackDate : int
    ackData = models.IntegerField()
    # - author : string
    author = models.TextField()
    # - category : string [*]
    category = ListField()
    # - feedURL : string
    category = models.TextField()
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
    pubDate = models.DateField()
    # - contributor : string
    contributor = models.TextField()
    # - updated : date
    updated = models.DateField()

# Create your models here.
class Feed(models.Model):
    # Attributes
    # - URL : string
    URL = models.TextField()
    # - logo : (string, string, string)
    # - title : string
    title = models.TextField()
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
    ttl = models.IntegerField()
    # - logo : string
    logo = models.TextField()
    # - skipDays : int
    skipDays = models.IntegerField()
    # - skipHours : int
    skipHours = models.IntegerField()
    # - author : string
    author = models.TextField()
    # - contributor : string
    contributor = models.TextField()
    # - guid : string
    guid = models.TextField()

    # Methods
    def getPosts(self, n):
        pass

    def getAll(self):
        pass

    def getSize(self):
        pass
