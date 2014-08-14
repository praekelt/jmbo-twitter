from django.contrib import admin
from django.core.urlresolvers import reverse, NoReverseMatch

from jmbo.admin import ModelBaseAdmin

from jmbo_twitter import models


class FeedAdmin(ModelBaseAdmin):
    inlines = []
    list_display = ('title', '_image', 'subtitle', 'publish_on', 'retract_on', \
        '_get_absolute_url', 'owner', 'created', '_actions'
    )

    def _image(self, obj):
        if obj.profile_image_url:
            return '<img src="%s" />' % obj.profile_image_url
        else:
            return ''
    _image.short_description = 'Image'
    _image.allow_tags = True

    def _actions(self, obj):
        # Once a newer version of jmbo is out the try-except can be removed
        try:
            parent = super(FeedAdmin, self)._actions(obj)
        except AttributeError:
            parent = ''

        try:
            url = reverse('feed-fetch-force', args=[obj.id]),
            one = '<a href="%s">Fetch tweets</a>' % url
        except NoReverseMatch:
            one = "Fetch tweets - add jmbo_twitter admin_urls to settings, eg. <code>(r'^admin/', include('jmbo_twitter.admin_urls'))</code>"

        try:
            url = reverse('feed-tweets', args=[obj.id]),
            two = '<a href="%s" target="_blank">View tweets</a>' % url
        except NoReverseMatch:
            two = "View tweets - add jmbo_twitter admin_urls to settings, eg. <code>(r'^admin/', include('jmbo_twitter.admin_urls'))</code>"

        return parent + '<ul><li>' + one + '</li><li>' + two + '</li></ul>'
    _actions.short_description = 'Actions'
    _actions.allow_tags = True


class SearchAdmin(ModelBaseAdmin):
    inlines = []
    list_display = ('title', 'subtitle', 'criteria', 'publish_on', 'retract_on', \
        '_get_absolute_url', 'owner', 'created', '_actions'
    )

    def _actions(self, obj):
        # Once a newer version of jmbo is out the try-except can be removed
        try:
            parent = super(SearchAdmin, self)._actions(obj)
        except AttributeError:
            parent = ''

        try:
            url = reverse('search-fetch-force', args=[obj.id]),
            one = '<a href="%s">Fetch tweets</a>' % url
        except NoReverseMatch:
            one = "Fetch tweets - add jmbo_twitter admin_urls to settings, eg. <code>(r'^admin/', include('jmbo_twitter.admin_urls'))</code>"

        try:
            url = reverse('search-tweets', args=[obj.id]),
            two = '<a href="%s" target="_blank">View tweets</a>' % url
        except NoReverseMatch:
            two = "View tweets - add jmbo_twitter admin_urls to settings, eg. <code>(r'^admin/', include('jmbo_twitter.admin_urls'))</code>"

        return parent + '<ul><li>' + one + '</li><li>' + two + '</li></ul>'
    _actions.short_description = 'Actions'
    _actions.allow_tags = True


admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.Search, SearchAdmin)
