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
            statuses = api.GetUserTimeline(self.name)
        except URLError:
            statuses = []
        except ValueError:
            statuses= []
        except twitter.TwitterError:
            # Happens when user is not on twitter anymore
            statuses = []

        print statuses
        updates = []
        keys = ('created_at', 'text', 'name', 'profile_image_url')
        for status in statuses:
            # Discard keys we're not interested in. Need to do this since 
            # memcache values have a max size.
            di = {}
            for key in keys:
                di[key] = getattr(status, key, '%s not found' % key)
            di['created_at'] = datetime.datetime.fromtimestamp(status.created_at_in_seconds)
            updates.append(di)

        print updates
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

        cache.set(cache_key, updates, 30)
        return updates

    @property
    def updates(self):
        return self.fetch()
