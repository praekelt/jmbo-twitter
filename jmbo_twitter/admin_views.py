from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from jmbo_twitter.models import Feed


@staff_member_required
def feed_fetch_force(request, name, redirect_to):
    """Forcibly fetch tweets for the feed"""
    feed = Feed.objects.get(name=name)
    feed.fetch(force=True)
    request.user.message_set.create(
        message="Fetched tweets for %s" % feed.name
    )
    return HttpResponseRedirect(redirect_to)


@staff_member_required
def feed_tweets(request, name):
    extra = dict(object=Feed.objects.get(name=name))
    return render_to_response('admin/jmbo_twitter/feed_tweets.html', extra, context_instance=RequestContext(request))
