from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    '',
    url(r'^feed/(?P<slug>[\w-]+)/$', 'jmbo.views.object_detail', name='feed_object_detail'),
    url(r'^search/(?P<slug>[\w-]+)/$', 'jmbo.views.object_detail', name='search_object_detail'),
)
