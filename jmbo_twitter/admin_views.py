from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

from jmbo_twitter.models import Feed


@staff_member_required
def feed_fetch_force(request, feed_id, redirect_to):
    """Forcibly fetch updates for the feed"""
    feed = Feed.objects.get(id=feed_id)
    feed.fetch(force=True)
    request.user.message_set.create(
        message="Fetched updates for %s" % feed.name
    )
    return HttpResponseRedirect(redirect_to)
