from celery.decorators import periodic_task

from jmbo_twitter.models import Feed


@periodic_task(run_every=crontab(hour='*', minute='*/10', day_of_week='*'))
def fetch_feeds():
    for feed in Feed.objects.all():
        feed.fetch()
