# -*- coding:utf-8 -*-

import os
import time
import datetime
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.models import ApiKey
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication

from django.contrib.auth.models import User
from django.db import models

from tastypie.models import create_api_key
from tastypie.exceptions import Unauthorized

from PIL import Image
from django.conf import settings

from sorl.thumbnail import get_thumbnail
from pin.models import Post, Likes, Category, Notif, Comments,\
    Notif_actors, App_data, Stream
from user_profile.models import Profile
from pin.templatetags.pin_tags import get_username
from daddy_avatar.templatetags import daddy_avatar

from pin.tools import userdata_cache

models.signals.post_save.connect(create_api_key, sender=User)

CACHE_AVATAR = 0
CACHE_USERNAME = 1


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        excludes = ['password', 'email', 'is_superuser', 'is_staff',
                    'is_active']


class AppResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = App_data.objects.all()
        resource_name = "app"
        paginator_class = Paginator
        filtering = {
            "current": ('exact'),
        }


class ProfileObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        #return object_list.filter(user=bundle.request.user)
        return object_list

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        #return bundle.obj.user == bundle.request.user
        return object_list

    def create_list(self, object_list, bundle):
        # Assuming their auto-aassigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")
        #pass

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
        #pass


class ProfileResource(ModelResource):
    user = fields.IntegerField(attribute='user__id')
    user_name = fields.CharField(attribute='user__username')

    class Meta:
        allowed_methods = ['get']
        ordering = ['score']
        queryset = Profile.objects.all()
        resource_name = "profile"
        paginator_class = Paginator
        #cache = SimpleCache()
        #authentication = ApiKeyAuthentication()
        #authorization = ProfileObjectsOnlyAuthorization()
        filtering = {
            "user": ('exact'),
        }

    def dehydrate(self, bundle):
        user = bundle.data['user']
        bundle.data['user_avatar'] = userdata_cache(user, CACHE_AVATAR, size=300)
        return bundle


class CategotyResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = "category"
        #cache = SimpleCache()


class LikesResource(ModelResource):
    user_url = fields.IntegerField(attribute='user__id', null=True)
    post_id = fields.IntegerField(attribute='post_id', null=True)

    class Meta:
        queryset = Likes.objects.all()
        resource_name = 'likes'
        excludes = ['ip', 'id']
        filtering = {
            "post_id": ("exact",),
        }

    def dehydrate(self, bundle):
        user = bundle.data['user_url']
        bundle.data['user_avatar'] = userdata_cache(user, CACHE_AVATAR)
        bundle.data['user_name'] = userdata_cache(user, CACHE_USERNAME)

        return bundle


class CommentResource(ModelResource):
    user_url = fields.IntegerField(attribute='user_id', null=True)
    object_pk = fields.IntegerField(attribute='object_pk_id', null=True)

    class Meta:
        allowed_methods = ['get']
        queryset = Comments.objects.filter(is_public=True)
        resource_name = "comments"
        paginator_class = Paginator
        #fields = ['id', 'comment', 'object_pk', 'user_id', 'score', 'submit_date']
        excludes = ['ip_address', 'is_public', 'object_pk', 'reported']
        cache = SimpleCache(timeout=120)
        #limit = 1000
        filtering = {
            "object_pk": ('exact',),
        }

    def dehydrate(self, bundle):
        user = bundle.data['user_url']

        bundle.data['user_avatar'] = userdata_cache(user, CACHE_AVATAR)
        bundle.data['user_name'] = userdata_cache(user, CACHE_USERNAME)
        return bundle


class PostResource(ModelResource):
    thumb_default_size = "100x100"
    thumb_size = "100x100"
    thumb_crop = 'center'
    thumb_quality = 99
    thumb_query_name = 'thumb_size'
    #user_name = fields.CharField(attribute='user__username')
    #user_avatar = fields.CharField(attribute='user__email')
    user = fields.IntegerField(attribute='user_id')
    likers = fields.ListField()
    like = fields.IntegerField(attribute='cnt_like')
    category = fields.ToOneField(CategotyResource, 'category', full=True)

    like_with_user = fields.BooleanField(default=False)
    popular = None
    just_image = 0
    cur_user = None
    show_ads = True
    dispatch_exec = False

    class Meta:
        queryset = Post.objects.filter(status=1).order_by('-is_ads', '-id')
        resource_name = 'post'
        allowed_methods = ['get']
        paginator_class = Paginator
        fields = ['id', 'image', 'like', 'text', 'url', 'cnt_comment']
        #cache = SimpleCache()

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(PostResource, self)\
            .apply_filters(request, applicable_filters)
        userid = request.GET.get('user_id', None)
        category_id = request.GET.get('category_id', None)
        before = request.GET.get('before', None)
        popular = request.GET.get('popular', None)
        filters = {}

        if userid:
            filters.update(dict(user_id=userid))
            self.show_ads = False

        if category_id:
            category_ids = category_id.replace(',', ' ').split(' ')
            filters.update(dict(category_id__in=category_ids))
            self.show_ads = True

        if before:
            filters.update(dict(id__lt=before))
            self.show_ads = True

        if popular:
            self.show_ads = False
            date_from = None
            dn = datetime.datetime.now()
            if popular == 'month':
                date_from = dn - datetime.timedelta(days=30)
            elif popular == 'lastday':
                date_from = dn - datetime.timedelta(days=1)
            elif popular == 'lastweek':
                date_from = dn - datetime.timedelta(days=7)
            elif popular == 'lasteigth':
                date_from = dn - datetime.timedelta(hours=8)

            if date_from:
                start_from = time.mktime(date_from.timetuple())
                filters.update(dict(timestamp__gt=start_from))

        return base_object_list.filter(**filters).distinct()

    def apply_sorting(self, object_list, options=None):
        base_object_list = super(PostResource, self).apply_sorting(object_list)
        sorts = []
        sorts.append('-is_ads')

        if self.popular in ['month', 'lastday', 'lastweek', 'lasteigth']:
            sorts.append("-cnt_like")
        else:
            sorts.append('-id')
        sorts.append('-is_ads')

        return base_object_list.order_by(*sorts)

    def pre_dispatch(self, request, token_name):
        self.dispatch_exec = True
        token = request.GET.get(token_name, '')
        if token:
            try:
                api = ApiKey.objects.get(key=token)
                self.cur_user = api.user
            except:
                pass

        self.thumb_size = request.GET.get(self.thumb_query_name,
                                          self.thumb_default_size)
        self.just_image = request.GET.get('just_image', 0)
        self.popular = request.GET.get('popular', None)

    def dispatch(self, request_type, request, **kwargs):
        self.dispatch_exec = True
        self.pre_dispatch(request, 'token')

        return super(PostResource, self)\
            .dispatch(request_type, request, **kwargs)

    def dehydrate(self, bundle):
        if self.dispatch_exec is False:
            self.pre_dispatch(bundle.request, 'api_key')
    
        id = bundle.data['id']
        o_image = bundle.data['image']

        try:
            im = get_thumbnail(o_image,
                               self.thumb_size,
                               quality=self.thumb_quality,
                               upscale=False)
        except:
            im = ""

        if im:
            bundle.data['thumbnail'] = im
            bundle.data['hw'] = "%sx%s" % (im.height, im.width)

        if int(self.just_image) == 1:
            for key in ['user', 'url', 'like', 'like_with_user',
                        'cnt_comment', 'category', 'text',
                        'image', 'likers', 'resource_uri']:
                del(bundle.data[key])

            return bundle

        bundle.data['permalink'] = '/pin/%d/' % (int(id))
        user = bundle.data['user']
        bundle.data['user_avatar'] = userdata_cache(user, CACHE_AVATAR)
        #print self.cur_user
        if self.cur_user:
            if Likes.objects.filter(post_id=id, user=self.cur_user).count():
                bundle.data['like_with_user'] = True

        bundle.data['user_name'] = userdata_cache(user, CACHE_USERNAME)
        if bundle.data['like'] == -1:
            bundle.data['like'] = 0

        if bundle.data['cnt_comment'] == -1:
            bundle.data['cnt_comment'] = 0

        if self.get_resource_uri(bundle) == bundle.request.path:
            # this is detail
            img_path = os.path.join(settings.MEDIA_ROOT, o_image)
            im = Image.open(img_path)
            w, h = im.size
            bundle.data['large_hw'] = "%sx%s" % (h, w)

            bundle.data['likers'] = []
        return bundle


class NotifAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        Notif.objects.filter(user=bundle.request.user).update(seen=True)
        return object_list.filter(user=bundle.request.user)


class NotifyResource(ModelResource):
    actors = fields.ListField()
    image = fields.CharField(attribute='post__image')
    like = fields.IntegerField(attribute='post__cnt_like')
    cnt_comment = fields.IntegerField(attribute='post__cnt_comment')
    text = fields.CharField(attribute='post__text')
    url = fields.CharField(attribute='post__url')
    post_id = fields.IntegerField(attribute='post_id')
    user_id = fields.IntegerField(attribute='user_id')
    post_owner_id = fields.IntegerField(attribute='post__user_id')
    category = fields.ToOneField(CategotyResource, 'post__category', full=True)
    like_with_user = fields.BooleanField(default=False)
    cur_user = None
    post = fields.ToOneField(PostResource, 'post')

    class Meta:
        resource_name = 'notify'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = NotifAuthorization()
        queryset = Notif.objects.all().order_by('-date')
        paginator_class = Paginator
        #cache = SimpleCache()
        filtering = {
            #"user_id": ('exact',),
            "seen": ('exact',),
        }

    def apply_authorization_limits(self, request, object_list):
        #print "hello"

        return object_list.filter(user=request.user)

    def dispatch(self, request_type, request, **kwargs):
        token = request.GET.get('token', '')
        if token:
            try:
                api = ApiKey.objects.get(key=token)
                self.cur_user = api.user
            except:
                pass

        return super(NotifyResource, self)\
            .dispatch(request_type, request, **kwargs)

    def dehydrate(self, bundle):
        id = bundle.data['id']
        o_image = bundle.data['image']
        try:
            im = get_thumbnail(o_image, "300x300", quality=99, upscale=False)
        except:
            im = ""

        if im:
            bundle.data['thumbnail'] = im
            bundle.data['hw'] = "%sx%s" % (im.height, im.width)

        if self.cur_user:
            if Likes.objects.filter(post_id=bundle.data['post_id'],
                                    user=self.cur_user).count():
                bundle.data['like_with_user'] = True

        post_owner_id = bundle.data['post_owner_id']

        bundle.data['post_owner_avatar'] = userdata_cache(post_owner_id, CACHE_AVATAR)
        bundle.data['post_owner_user_name'] = userdata_cache(post_owner_id, CACHE_USERNAME)

        actors = Notif_actors.objects.filter(notif=id).order_by('id')[:10]
        ar = []
        for lk in actors:
            ar.append(
                [
                    lk.actor.id,
                    get_username(lk.actor),
                    daddy_avatar.get_avatar(lk.actor, size=100)
                ]
            )

        bundle.data['actors'] = ar

        return bundle


class StreamAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)


class StreamResource(ModelResource):
    post = fields.ForeignKey(PostResource, 'post', full=True)

    class Meta:
        queryset = Stream.objects.all().order_by('-date')
        authentication = ApiKeyAuthentication()
        authorization = StreamAuthorization()
