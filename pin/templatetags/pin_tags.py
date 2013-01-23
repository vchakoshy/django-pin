import datetime
from calverter import Calverter
from urlparse import urlparse

from django import template
from django.contrib.auth.models import User
from django.template import Library,Node
from django.template.base import TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe

from pin.models import Likes as pin_likes, Notify, Category
from user_profile.models import Profile

register = Library()

def user_cats(parser, token):
   
    return UserCats()

class UserCats(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        try:
            user = context['user']
            subs = Category.objects.filter(user=user).all()
            if subs:
                context['user_category'] = subs
                #return 1
            else:
                context['user_category'] = []
                #return 0
        except template.VariableDoesNotExist:
            return ''
        
        return ''
    
register.tag('user_cats', user_cats)


def user_item_like(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, item = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    
    return UserItemLike(item)

class UserItemLike(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            item = int(self.item.resolve(context))
            user=context['user']
            liked = Likes.objects.filter(user=user, item=item).count()
            if liked :
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
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    
    return UserPostLike(item)

class UserPostLike(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            item = int(self.item.resolve(context))
            user=context['user']
            liked = pin_likes.objects.filter(user=user, post=item).count()
            if liked :
                return 'btn-danger'
            else:
                return ''
        except template.VariableDoesNotExist:
            return ''

register.tag('user_post_like', user_post_like)

@register.filter
def get_user_notify(userid):
    notify = Notify.objects.all().filter(user_id=userid, seen=False).count()
    return notify

@register.filter
def get_username(user):
    try:
        profile=Profile.objects.get(user_id=user.id)
        username=profile.name
    except Profile.DoesNotExist:
        username=user.username
    return username

@register.filter
def get_host(value):
    o = urlparse(value)
    if hasattr(o, 'netloc'):
        return o.netloc
    else:
        return ''

@register.filter
def date_from_timestamp(value):
    return datetime.datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')

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
