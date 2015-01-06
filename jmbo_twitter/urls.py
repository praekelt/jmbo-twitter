from django.conf.urls import patterns, url

from jmbo.views import ObjectDetail


urlpatterns = patterns(
    '',
    url(r'^feed/(?P<slug>[\w-]+)/$', ObjectDetail.as_view(), name='feed_object_detail'),
    url(r'^search/(?P<slug>[\w-]+)/$', ObjectDetail.as_view(), name='search_object_detail'),
)
