from django.core import management
from django.test import TestCase as BaseTestCase
from django.test.client import Client as BaseClient, RequestFactory
from django.contrib.auth.models import User

from twitter import Status

from jmbo_twitter.models import Feed, Search


class FakeAPI(object):

    def GetUserTimeline(self, screen_name=None, include_rts=None):
        return [Status(text='status')]

    def GetSearch(self, term=None):
        return [Status(text='search')]


class TestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = RequestFactory()
        cls.client = BaseClient()

        # Editor
        cls.editor, dc = User.objects.get_or_create(
            username='editor',
            email='editor@test.com'
        )
        cls.editor.set_password("password")
        cls.editor.save()

        # Feed
        obj, dc = Feed.objects.get_or_create(
            title='Twitter', name='twitter',
            owner=cls.editor, state='published',
        )
        obj.sites = [1]
        obj.save()
        cls.feed = obj

        # Search
        obj, dc = Search.objects.get_or_create(
            title='Wtf', criteria='#wtf',
            owner=cls.editor, state='published',
        )
        obj.sites = [1]
        obj.save()
        cls.search = obj

        cls.fakeapi = FakeAPI()

    def test_feed_get_statuses(self):
        statuses = self.feed.get_statuses(self.fakeapi)
        self.assertEqual(len(statuses), 1)

    def test_search_get_statuses(self):
        statuses = self.search.get_statuses(self.fakeapi)
        self.assertEqual(len(statuses), 1)

    def test_feed_detail_view(self):
        response = self.client.get(self.feed.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_search_detail_view(self):
        response = self.client.get(self.search.get_absolute_url())
        self.assertEqual(response.status_code, 200)
