import datetime, re, twitter
from urllib2 import URLError

from django.db import models
from django.core.cache import cache


class Feed(models.Model):
    """A feed represents  a twitter user account""" 
    name = models.CharField(
        max_length=50, 
        unique=True,
        help_text="A twitter account name, eg. johnsmith"
    )
    full_name = models.CharField(max_length=255, help_text="The display name")
    profile_image_url = models.CharField(
        null=True, editable=False, max_length=255
    )

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def fetch(self, force=False):
        cache_key = 'jmbo_twitter_feed_%s' % self.name
        cached = cache.get(cache_key, None)
        if cached is not None:
            return cached

        # Query twitter taking care to handle network errors
        api = twitter.Api()
        try:
            statuses = api.GetUserTimeline(self.name, include_rts=True)
        except URLError:
            statuses = []
        except ValueError:
            statuses= []
        except twitter.TwitterError:
            # Happens when user is not on twitter anymore
            statuses = []

        for status in statuses:
            status.created_at = datetime.datetime.fromtimestamp(
                status.created_at_in_seconds
            )
        
        if statuses:
            # This is also a convenient place to set the feed image url
            status = statuses[0]
            changed = False
            if status.user.profile_image_url != self.profile_image_url:
                self.profile_image_url = status.user.profile_image_url
                changed = True
            if status.user.name != self.full_name:
                self.full_name = status.user.name
                changed = True
            if changed:
                self.save()

        cache.set(cache_key, statuses, 1200)
        return statuses

    @property
    def tweets(self):
        return self.fetch()
