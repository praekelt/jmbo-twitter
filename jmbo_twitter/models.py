import datetime, twitter
from urllib2 import URLError

from django.db import models
from django.core.cache import cache

from jmbo.models import ModelBase


class Status(ModelBase):
    """Purely a wrapper that allows us to use jmbo-foundry's listings for 
    tweets."""
    def __init__(self, status):
        # Copy attributes over
        attrs = ('contributors', 'coordinates', 'created_at', \
            'created_at_in_seconds', 'favorited', 'geo', 'hashtags', 'id', \
            'in_reply_to_screen_name', 'in_reply_to_status_id', \
            'in_reply_to_user_id', 'location', 'now', 'place', \
            'relative_created_at', 'retweet_count', 'retweeted', \
            'retweeted_status', 'source', 'text', 'truncated', 'urls', 'user', \
            'user_mentions', 'created_at_datetime')
        for attr in attrs:            
            setattr(self, attr, getattr(status, attr))

    @property
    def as_leaf_class(self):
        return self

    def save(self):
        raise NotImplemented


class Feed(ModelBase):
    """A feed represents  a twitter user account""" 
    name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="A twitter account name, eg. johnsmith"
    )
    profile_image_url = models.CharField(
        null=True, editable=False, max_length=255
    )

    def save(self, *args, **kwargs):
        self.slug = self.name
        super(ModelBase, self).save(*args, **kwargs)

    def fetch(self, force=False):
        cache_key = 'jmbo_twitter_feed_%s' % self.slug
        cached = cache.get(cache_key, None)
        if cached is not None:
            return cached

        # Query twitter taking care to handle network errors
        api = twitter.Api()
        try:
            statuses = api.GetUserTimeline(self.slug, include_rts=True)
        except URLError:
            statuses = []
        except ValueError:
            statuses= []
        except twitter.TwitterError:
            # Happens when user is not on twitter anymore
            statuses = []

        for status in statuses:
            status.created_at_datetime = datetime.datetime.fromtimestamp(
                status.created_at_in_seconds
            )
       
        if statuses:
            # This is also a convenient place to set the feed image url
            status = statuses[0]
            changed = False
            if status.user.profile_image_url != self.profile_image_url:
                self.profile_image_url = status.user.profile_image_url
                changed = True
            if status.user.name != self.title:
                self.title = status.user.name
                changed = True
            if changed:
                self.save()

        cache.set(cache_key, statuses, 1200)
        return statuses

    @property
    def tweets(self):
        class MyList(list):
            """Slightly emulate QuerySet API so jmbo-foundry listings work"""

            @property
            def exists(self):
                return len(self) > 0

        result = []
        for status in self.fetch():
            result.append(Status(status))

        return MyList(result)
