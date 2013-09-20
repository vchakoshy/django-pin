import datetime
from calverter import Calverter
from urlparse import urlparse

from django import template
from django.contrib.auth.models import User
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe

from pin.models import Likes as pin_likes, Notif
from user_profile.models import Profile

from pin.tools import userdata_cache


register = Library()


def user_item_like(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, item = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments"
            % token.contents.split()[0])

    return UserItemLike(item)


class UserItemLike(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            item = int(self.item.resolve(context))
            user = context['user']
            liked = pin_likes.objects.filter(user=user, item=item).count()
            if liked:
                return 'btn-danger'
            else:
                return ''
        except template.VariableDoesNotExist:
            return ''

register.tag('user_item_like', user_item_like)


def user_post_like(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, item = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments"
            % token.contents.split()[0])

    return UserPostLike(item)


class UserPostLike(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            item = int(self.item.resolve(context))
            user = context['user']
            liked = pin_likes.objects.filter(user=user, post=item).count()
            if liked:
                return 'btn-danger'
            else:
                return ''
        except template.VariableDoesNotExist:
            return ''

register.tag('user_post_like', user_post_like)


@register.filter
def get_user_notify(userid):
    print "user id ", userid
    notify = Notif.objects.all().filter(user_id=userid, seen=False).count()
    return notify


@register.filter
def get_username(user):
    if isinstance(user, int):
        user = User.objects.only('username').get(pk=user)

    try:
        profile = Profile.objects.only('name').get(user_id=user.id)
        if not profile:
            username = user.username
        else:
            username = profile.name
    except Profile.DoesNotExist:
        username = user.username

    if not username:
        username = user.username

    return username


@register.filter
def get_userdata_avatar(user, size=30):
    #print "size is: ",  user, size
    return userdata_cache(user, 0, size=size)


@register.filter
def get_userdata_name(user, size=30):
    return userdata_cache(user, 1)


@register.filter
def get_host(value):
    o = urlparse(value)
    if hasattr(o, 'netloc'):
        return o.netloc
    else:
        return ''


@register.filter
def date_from_timestamp(value):
    return datetime.datetime.fromtimestamp(int(value))\
        .strftime('%Y-%m-%d %H:%M:%S')


@register.filter
def jalali_mysql_date(value):
    #gd = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    gd = value
    cal = Calverter()
    jd = cal.gregorian_to_jd(gd.year, gd.month, gd.day)

    d = cal.jd_to_jalali(jd)
    d = "%s/%s/%s" % (d[0], d[1], d[2])
    return d


def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))
remove_newlines.is_safe = True
remove_newlines = stringfilter(remove_newlines)
register.filter(remove_newlines)
