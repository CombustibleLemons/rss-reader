from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

from main.api import UserList, UserDetail, UserTopicList
from main.api import TopicList, TopicDetail, TopicFeedList
from main.api import FeedList, FeedDetail, FeedPostList, feed_create
from main.api import PostList, PostDetail

user_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', UserTopicList.as_view(), name='userfeed-list'),
    url(r'^/(?P<pk>[0-9]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^/$', UserList.as_view(), name='user-list')
)
topic_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', TopicFeedList.as_view(), name='topicfeed-list'),
    url(r'^/(?P<pk>[0-9]+)$', TopicDetail.as_view(), name='topic-detail'),
    url(r'^/$', TopicList.as_view(), name='topic-list')
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
    url(r'^users', include(user_urls)),
    url(r'^topics', include(topic_urls)),
    url(r'^feeds', include(feed_urls)),
    url(r'^posts', include(post_urls)),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
)
