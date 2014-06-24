import datetime, twitter
from urllib2 import URLError
import logging

from django.db import models
from django.core.cache import cache
from django.conf import settings

from jmbo.models import ModelBase


logger = logging.getLogger('django')


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
    """A feed represents a twitter user account"""
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="A twitter account name, eg. johnsmith"
    )
    profile_image_url = models.CharField(
        null=True, editable=False, max_length=255
    )
    twitter_id = models.CharField(max_length=255, default='', editable=False)

    def fetch(self, force=False):
        cache_key = 'jmbo_twitter_feed_%s' % self.id
        cached = cache.get(cache_key, None)
        if (cached is not None) and not force:
            return cached

        # Get and check settings
        di = getattr(settings, 'JMBO_TWITTER', {})
        ck = di.get('consumer_key')
        cs = di.get('consumer_secret')
        atk = di.get('access_token_key')
        ats = di.get('access_token_secret')
        if not all([ck, cs, atk, ats]):
            logger.error(
                'jmbo_twitter.models.Feed.fetch - incomplete settings'
            )
            return []

        # Query twitter taking care to handle network errors
        api = twitter.Api(
            consumer_key=ck, consumer_secret=cs, access_token_key=atk,
            access_token_secret=ats
        )
        try:
            # Fall back to slug for historical reasons
            statuses = api.GetUserTimeline(
                screen_name=self.name or self.slug, include_rts=True
            )
        except URLError:
            statuses = []
        except ValueError:
            statuses= []
        except twitter.TwitterError:
            # Happens when user is not on twitter anymore
            statuses = []
        except Exception, e:
            # All manner of things can go wrong with integration
            logger.error('jmbo_twitter.models.Feed.fetch - ' + e.message)
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

            # Only set if there are statuses. Twitter may randomly throttle use
            # and destroy our cache without this check.
            cache.set(cache_key, statuses, 1200)

        # Legacy return
        return statuses

    @property
    def fetched(self):
        cache_key = 'jmbo_twitter_feed_%s' % self.id
        return cache.get(cache_key, [])

    @property
    def tweets(self):
        class MyList(list):
            """Slightly emulate QuerySet API so jmbo-foundry listings work"""

            @property
            def exists(self):
                return len(self) > 0

        result = []
        for status in self.fetched:
            result.append(Status(status))

        return MyList(result)
