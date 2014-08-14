from celery.decorators import periodic_task
from celery.task.schedules import crontab

from jmbo_twitter.models import Feed, Search


@periodic_task(run_every=crontab(hour='*', minute='*/15', day_of_week='*'))
def fetch_feeds():
    for feed in Feed.objects.all():
        feed.fetch(force=True)


@periodic_task(run_every=crontab(hour='*', minute='*/15', day_of_week='*'))
def fetch_searchs():
    for search in Search.objects.all():
        search.fetch(force=True)
