from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

from main.api import *

#urls for login and logout. not sure what to name them.
account_urls = patterns('',
    url(r'^/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^/logout/$', 'django.contrib.auth.views.logout_then_login',name="logout"),
    url(r'^/register/$', MainViews.register, name="logout")
)

user_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', UserTopicList.as_view(), name='userfeed-list'),
    url(r'^/(?P<pk>[0-9]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^/$', UserList.as_view(), name='user-list')
)
topic_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', TopicFeedList.as_view(), name='topicfeed-list'),
    url(r'^/(?P<pk>[0-9]+)$', TopicDetail.as_view(), name='topic-detail'),
    url(r'^/$', TopicList.as_view(), name='topic-list'),
    url(r'^/create$', topic_create, name='topic-create'),
    url(r'^/delete$', topic_delete, name='topic-delete'),
    url(r'^/rename$', topic_rename, name='topic-rename'),
)

feed_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', FeedPostList.as_view(), name='feedpost-list'),
    url(r'^/(?P<pk>[0-9]+)$', FeedDetail.as_view(), name='feed-detail'),
    url(r'^/create$', feed_create, name='feed-create'),
    url(r'^/$', FeedList.as_view(), name='feed-list')
)

post_urls = patterns('',
    url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
    url(r'^/$', PostList.as_view(), name='post-list')
)

urlpatterns = patterns('',
    # Djangular internals
    url(r'^djangular/', include('djangular.urls')),

    # REST API
    url(r'^account', include(account_urls)),
    url(r'^users', include(user_urls)),
    url(r'^topics', include(topic_urls)),
    url(r'^feeds', include(feed_urls)),
    url(r'^posts', include(post_urls)),

    # Searching
    url(r'^search/', search, name='search-for-feed'),

    # Rest API Auth
    url(r'^rest-auth/', include('rest_auth.urls')),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

	# Main
    url(r'^', MainViews.index),

   )
