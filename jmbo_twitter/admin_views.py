from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _

from jmbo_twitter.models import Feed, Search


@staff_member_required
def feed_fetch_force(request, id, redirect_to):
    """Forcibly fetch tweets for the feed"""
    feed = Feed.objects.get(id=id)
    feed.fetch(force=True)
    msg = _("Fetched tweets for %s" % feed.name)
    messages.success(request, msg, fail_silently=True)
    return HttpResponseRedirect(redirect_to)


@staff_member_required
def feed_tweets(request, id):
    extra = dict(object=Feed.objects.get(id=id))
    return render_to_response(
        'admin/jmbo_twitter/feed_tweets.html',
        extra,
        context_instance=RequestContext(request)
    )


@staff_member_required
def search_fetch_force(request, id, redirect_to):
    """Forcibly fetch tweets for the search"""
    search = Search.objects.get(id=id)
    search.fetch(force=True)
    msg = _("Fetched tweets for %s" % search.criteria)
    messages.success(request, msg, fail_silently=True)
    return HttpResponseRedirect(redirect_to)


@staff_member_required
def search_tweets(request, id):
    extra = dict(object=Search.objects.get(id=id))
    return render_to_response(
        'admin/jmbo_twitter/feed_tweets.html',
        extra,
        context_instance=RequestContext(request)
    )
