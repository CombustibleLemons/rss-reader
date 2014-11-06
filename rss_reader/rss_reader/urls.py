from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

from main.api import FeedList, FeedDetail, FeedPostList, feed_create
from main.api import PostList, PostDetail

feed_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/posts$', FeedPostList.as_view(), name='feedpost-list'),
    url(r'^/(?P<pk>[0-9]+)$', FeedDetail.as_view(), name='feed-detail'),
    url(r'^/create$', feed_create, name='feed-create'),
    url(r'^/$', FeedList.as_view(), name='feed-list')
)

post_urls = patterns('',
    #url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
    url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
    url(r'^$', PostList.as_view(), name='post-list')
)

# from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
# from main.api import FeedList, FeedDetail
#
# urlpatterns = [
#     url(r'^feeds/$', FeedList.as_view()),
#     url(r'^feeds/(?P<pk>[0-9]+)/$', FeedDetail.as_view()),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rss_reader.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', MainViews.index),
    url(r'^djangular/', include('djangular.urls')),

    url(r'^feeds', include(feed_urls)),
    url(r'^posts', include(post_urls)),
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^', MainViews.index),

    # Login / logout.
    # (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # (r'^logout/$', MainViews.logout_page),

    # Web portal.
    # (r'^portal/', MainViews.portal_main_page),
)
