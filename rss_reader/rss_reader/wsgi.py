"""
WSGI config for rss_reader project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rss_reader.settings")

# DB update loop
import threading
import time
from main.models import Feed
def feedUpdater(feed):
    feed.update()

def worker():
    while True:
        print "Updating Feeds"
        for feed in Feed.objects.all():
            t = threading.Thread(target=feedUpdater, args=(feed,))
            t.start()
        print "Feeds updated"
        # Update every 5 minutes
        time.sleep(300)

t = threading.Thread(target=worker)
t.start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
