import datetime, twitter
from urllib2 import URLError
import logging

from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
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


class StatusMixin(object):

    def get_statuses(self, api):
        raise NotImplemented

    def fetch(self, force=False):
        klass_name = self.__class__.__name__
        cache_key = 'jmbo_twitter_%s_%s' % (klass_name, self.id)
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
                'jmbo_twitter.models.%s.fetch - incomplete settings' \
                    % klass_name
            )
            return []

        # Query twitter taking care to handle network errors
        api = twitter.Api(
            consumer_key=ck, consumer_secret=cs, access_token_key=atk,
            access_token_secret=ats
        )
        try:
            statuses = self.get_statuses(api)
        except (URLError, ValueError, twitter.TwitterError):
            statuses = []
        except Exception, e:
            # All manner of things can go wrong with integration
            logger.error(
                'jmbo_twitter.models.%s.fetch - %s' % (klass_name, e.message)
            )
            statuses = []

        for status in statuses:
            status.created_at_datetime = datetime.datetime.fromtimestamp(
                status.created_at_in_seconds
            )

        if statuses:
            # Only set if there are statuses. Twitter may randomly throttle us
            # and destroy our cache without this check. Cache for a long time
            # incase Twitter goes down.
            cache.set(cache_key, statuses, 86400)

        # Legacy return
        return statuses

    @property
    def fetched(self):
        klass_name = self.__class__.__name__
        cache_key = 'jmbo_twitter_%s_%s' % (klass_name, self.id)
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


class Feed(ModelBase, StatusMixin):
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

    def get_statuses(self, api):
        # Fall back to slug for historical reasons
        statuses = api.GetUserTimeline(
            screen_name=self.name or self.slug, include_rts=True
        )
        return statuses

    def fetch(self, force=False):
        statuses = super(Feed, self).fetch(force=force)

        if statuses:
            # This is a convenient place to set the feed image url
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

        return statuses


class Search(ModelBase, StatusMixin):
    """A search represents a twitter keyword search"""
    criteria = models.CharField(
        max_length=255,
        unique=True,
        help_text="Search string or a hashtag"
    )

    class Meta:
        verbose_name_plural = _("Searches")

    def get_statuses(self, api):
        return api.GetSearch(self.criteria)
