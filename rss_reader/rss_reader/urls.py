from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views as MainViews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rss_reader.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', MainViews.index),
)
