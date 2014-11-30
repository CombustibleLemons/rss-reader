# Callback function that fire on Django signals
from main.models import *

# Enforces validation of feeds that are to be added
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
def topicFeedsChanged(sender, instance, **kwargs):
    """ Validates a Topic so that no Topic can be modified that does not adhere to constraints"""
    # Remember to exclude self from the checking!
    import pdb; pdb.set_trace()
    if kwargs['action'] == 'pre_clear':
        # Create a list of the original feed pk_set
        instance.original_pk_set = [feed.id for feed in instance.feeds.all()]
    if kwargs['action'] == 'pre_add':
        # We have to keep track of a failed set, since just throwing a ValidationError would cause
        # the Topic objects to lose all of its feeds.
        failed = []
        duplicates = []
        pk_set = kwargs.pop("pk_set")
        for pk in pk_set:
            for t in instance.user.topics.all().exclude(id=instance.id):
                # Check if the feed is in any other topic
                if t.feeds.filter(id=pk).exists():
                    # Add the pk to failed list and remove it from the pk_set
                    failed.append(pk)
                    break
            # Check if feed is in this Topic's feed list
            if instance.original_pk_set:
                if pk in instance.original_pk_set:
                    # Present as warning to the user.
                    duplicates.append(pk)
        # Since we are forced to use Django signals, put the data into the object and remove it later
        instance.failed = failed
        instance.duplicates = duplicates
        del instance.original_pk_set
    elif kwargs['action'] == 'post_add':
     # Report any failed pks. See TODO above.
        failed = instance.failed
        if failed:
            errMsg = "Feeds %s already exists in another topic" % (str(failed),)
            # Remove failures
            instance.feeds.remove(*failed)
            raise ValidationError(errMsg)
        elif instance.duplicates:
            errMsg = "Feeds %s already exists in this topic" % (str(failed),)
            raise ValidationError(errMsg)
        # Cleanup the failed rider, don't want it sticking around with the object forever
        del instance.failed

        # Make sure each added feed is given a PostsRead object to associate with a User
        user = instance.user
        for feed in list(instance.feeds.all()):
            try:
                with transaction.atomic():
                    pr = PostsRead(user=user, feed=feed)
                    pr.save()
            except IntegrityError as e:
                # IntegrityError means one already exists, so pass
                pass

m2m_changed.connect(topicFeedsChanged, sender=Topic.feeds.through)

# Create 'Uncategorized' Topic to put stuff in on user creation
@receiver(post_save, sender=User)
def createUncategorized(sender, instance, **kwargs):
    """ Creates an Uncategorized topic for every User"""
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
# watson.register(Post.objects.all(), fields = ("title", "subtitle", "author", "content",))

def update_post_index(instance, **kwargs):
    """Updates the watson object index with the Post object"""
    for post in instance.posts.all():
        watson.default_search_engine.update_obj_index(post)

post_save.connect(update_post_index, Feed)
