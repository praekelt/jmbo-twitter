from django.conf.urls import patterns, include


urlpatterns = patterns(
    (r'^jmbo/', include('jmbo.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^jmbo_twitter/', include('jmbo_twitter.urls')),
)
