import re

from django import template

from django.utils.html import urlize
register = template.Library()


@register.filter(name='tweetify')
def tweetify(value):
    s = urlize(value)
    s = re.sub(r'(@[\w]+)', '<a href="http://twitter.com/\g<1>">\g<1></a>', s)
    return s
