from django.conf.urls.defaults import patterns, url, include

from jmbo_twitter.models import Feed


urlpatterns = patterns(
    '',

    url(
        r'^feed/(?P<slug>[\w-]+)/$', 
        'django.views.generic.list_detail.object_detail',
        {'queryset': Feed.permitted.all(), 'slug_field': 'name'},
        name='feed-detail'
    ),  

)
