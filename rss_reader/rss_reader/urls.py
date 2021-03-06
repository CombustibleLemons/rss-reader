from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

from main.api import *

# Debug URLs should circumvent username restrictions
debug_urls = patterns('',
    url(r'^/users$', UserDetail.as_view(), name='user-detail'),
)

# URLSs for login and logout. not sure what to name them.
account_urls = patterns('',
    url(r'^/login/$', MainViews.user_login, name="login"),
    url(r'^/logout/$', MainViews.user_logout,name="logout"),
    url(r'^/register/$', MainViews.register, name="register")
)

user_urls = patterns('',
    url(r'^/$', UserDetail.as_view(), name='user-list'),
    url(r'^/settings/$', UserSettingsDetail.as_view(), name='settings-detail')
)
topic_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)$', TopicDetail.as_view(), name='topic-detail'),
    url(r'^/$', TopicList.as_view(), name='topic-list')
)

feed_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts/read$', PostsReadDetail.as_view(), name='topic-read-posts-list'),
    url(r'^/(?P<pk>[0-9]+)/posts/unread$', unread_posts, name='topicfeed-unread-list'),
    url(r'^/(?P<pk>[0-9]+)/posts/$', FeedPostList.as_view(), name='feedpost-list'),
    url(r'^/(?P<pk>[0-9]+)$', FeedDetail.as_view(), name='feed-detail'),
    url(r'^/create/$', feed_create, name='feed-create')
)

queue_feed_urls = patterns('',
    url(r'^/create/(?P<pk>[0-9]+)/$', QueueFeedList.as_view(), name='queue-feed-list'),
    url(r'^/(?P<pk>[0-9]+)/$', QueueFeedDetail.as_view(), name='queue-feed-detail'),
    url(r'^/(?P<pk>[0-9]+)/posts/$', QueueFeedPostList.as_view(), name='queue-feed-post-list'),
)

urlpatterns = patterns('',
    # Djangular internals
    url(r'^djangular/', include('djangular.urls')),

    # REST API
    url(r'^accounts', include(account_urls)),
    url(r'^user', include(user_urls)),
    url(r'^topics', include(topic_urls)),
    url(r'^feeds', include(feed_urls)),
    url(r'^queue_feeds', include(queue_feed_urls)),

    # Searching
    url(r'^search/', search, name='search-for-feed'),

    # Debug urls
    url(r'^debug', include(debug_urls)),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

	# Main
    url(r'^$', MainViews.index),

   )
