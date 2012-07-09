from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',

    (
        r'^admin/jmbo_twitter/(?P<name>[\w-]+)/fetch-force/$',  
        'jmbo_twitter.admin_views.feed_fetch_force',
        {'redirect_to' : '/admin/jmbo_twitter/feed'},
        'feed-fetch-force',
    ),

    (
        r'^admin/jmbo_twitter/(?P<name>[\w-]+)/tweets/$',  
        'jmbo_twitter.admin_views.feed_tweets',
        {},
        'feed-tweets',
    ),

)
