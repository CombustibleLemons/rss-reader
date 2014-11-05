from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

from main.api import FeedList, FeedDetail, FeedPostList
from main.api import PostList, PostDetail

feed_urls = patterns('',
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/posts$', FeedPostList.as_view(), name='feedpost-list'),
    url(r'^/(?P<pk>[0-9a-zA-Z_\.]+)$', FeedDetail.as_view(), name='feed-detail'),
    url(r'^$', FeedList.as_view(), name='user-list')
)

post_urls = patterns('',
    #url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
    url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
    url(r'^$', PostList.as_view(), name='post-list')
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rss_reader.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^djangular/', include('djangular.urls')),

    url(r'^feeds', include(feed_urls)),
    url(r'^posts', include(post_urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', MainViews.index),

    # Login / logout.
    # (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # (r'^logout/$', MainViews.logout_page),

    # Web portal.
    # (r'^portal/', MainViews.portal_main_page),
)
