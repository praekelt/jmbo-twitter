from django.contrib import admin
from django.core.urlresolvers import reverse

from jmbo_twitter import models


class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', '_image', '_actions')

    def _image(self, obj):
        if obj.profile_image_url:
            return '<img src="%s" />' % obj.profile_image_url
        else:
            return ''
    _image.short_description = 'Image'
    _image.allow_tags = True

    def _actions(self, obj):
        return '''<ul>
            <li><a href="%s">Fetch tweets</a></li>
            <li><a href="%s">View tweets</a></li>
            </ul>''' % (
                reverse('feed-fetch-force', args=[obj.name]), 
                reverse('feed-tweets', args=[obj.name])
            )
    _actions.short_description = 'Actions'
    _actions.allow_tags = True


admin.site.register(models.Feed, FeedAdmin)
