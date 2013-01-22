# coding: utf-8
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from pin.models import Post

class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'

class LatestPinFeed(Feed):
    feed_type = CorrectMimeTypeFeed
    title = 'آخرین مطالب پین - ویسگون'
    link = "http://www.wisgoon.com/pin/"
    description = 'آخرین مطالب وارد شده در بخش پین وب سایت ویسگون'
    #creator = "http://www.wisgoon.com"
    
    def items(self):
        return Post.objects.order_by('-id')[:30]
    
    def item_title(self, item):
        return item.text[:80]
    
    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return reverse('pin-item', args=[item.pk])
    
    def item_pubdate(self, item):
        return item.create
    
    