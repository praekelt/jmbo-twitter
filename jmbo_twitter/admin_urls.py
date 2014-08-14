from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',

    (
        r'jmbo_twitter/feed/(?P<id>\d+)/fetch-force/$',
        'jmbo_twitter.admin_views.feed_fetch_force',
        {'redirect_to' : '/admin/jmbo_twitter/feed'},
        'feed-fetch-force',
    ),

    (
        r'^jmbo_twitter/feed/(?P<id>\d+)/tweets/$',
        'jmbo_twitter.admin_views.feed_tweets',
        {},
        'feed-tweets',
    ),

    (
        r'jmbo_twitter/search/(?P<id>\d+)/fetch-force/$',
        'jmbo_twitter.admin_views.search_fetch_force',
        {'redirect_to' : '/admin/jmbo_twitter/search'},
        'search-fetch-force',
    ),

    (
        r'^jmbo_twitter/search/(?P<id>\d+)/tweets/$',
        'jmbo_twitter.admin_views.search_tweets',
        {},
        'search-tweets',
    ),

)
