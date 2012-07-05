import datetime, re, twitter

from django.db import models


class Feed(models.Model):
    """A feed represents  a twitter user account""" 
    name = models.CharField(max_length=50, help_text="A twitter account name, eg. johnsmith", unique=True)
    full_name = models.CharField(max_length=255)
    profile_image_url = models.CharField(null=True, editable=False, max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    #@cache
    def fetch(self, force=False):

        # Query twitter taking care to handle network errors
        api = twitter.Api()
        try:
            updates = api.GetUserTimeline(self.name, since_id=self.last_fetched_id)
        except URLError:
            updates = []
        except ValueError:
            updates = []
        except twitter.TwitterError:
            # Happens when user is not on twitter anymore
            updates = []

        for update in updates:            
            fu = FeedUpdate(
                text=update.text[:140], 
                created_date=datetime.datetime.fromtimestamp(update.created_at_in_seconds),
                source=update.source[:255],
                feed=self
            )
            fu.save()        

        if updates:
            # This is also a convenient place to set the feed image url
            update = updates[0]
            changed = False
            if update.user.profile_image_url != self.profile_image_url:
                self.profile_image_url = update.user.profile_image_url
                changed = True
            if update.user.name != self.full_name:
                self.full_name = update.user.name
                changed = True
            if changed:
                self.save()
