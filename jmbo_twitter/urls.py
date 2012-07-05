from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',

    (
        r'^admin/jmbo_twitter/feed-fetch-force/(?P<feed_id>\d+)/$',  
        'jmbo_twitter.admin_views.feed_fetch_force',
        {'redirect_to' : '/admin/jmbo_twitter/feed'}
    ),

)
