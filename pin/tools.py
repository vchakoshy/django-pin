import os
import time
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
from user_profile.models import Profile

from daddy_avatar.templatetags import daddy_avatar

user_keys = {}
USERDATA_TIMEOUT = 300


def create_filename(filename):
    d = datetime.now()
    folder = "%d/%d" % (d.year, d.month)
    paths = []
    paths.append("%s/pin/temp/o/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/temp/t/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/images/o/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/images/t/" % (settings.MEDIA_ROOT))
    for path in paths:
        abs_path = "%s%s" % (path, folder)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
    filestr = "%s/%f" % (folder, time.time())
    filestr = filestr.replace('.', '')
    filename = "%s%s" % (filestr, os.path.splitext(filename)[1])
    return filename


def userdata_cache(user, field=None, size=100):
    cache_key = 'user_%s_%s' % (user, size)

    if cache_key in user_keys:
        data = user_keys[cache_key]
    else:
        data = cache.get(cache_key)

    if data:
        if field is not None:
            return data[field]

        return data
    else:
        avatar = daddy_avatar.get_avatar(user, size=size)
        username = get_username(user)

        value = [avatar, username]
        user_keys[cache_key] = value
        cache.set(cache_key, value, USERDATA_TIMEOUT)

        if field is not None:
            return value[field]

        return value

    return []


def get_username(user):
    if isinstance(user, (int, long)):
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


def get_request_timestamp(request):
    try:
        timestamp = int(request.GET.get('older', 0))
    except ValueError:
        timestamp = 0
    return timestamp


def get_user_ip(request):
    return request.META.get('REMOTE_ADDR', None)
