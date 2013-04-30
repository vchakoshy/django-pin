import os
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from tastypie import fields

from PIL import Image
from django.conf import settings

from sorl.thumbnail import get_thumbnail
from pin.models import Post, Likes
from daddy_avatar.templatetags import daddy_avatar

class LikesResource(ModelResource):
    class Meta:
        #queryset = Likes.objects.all()
        resource_name = 'likes'

class PostResource(ModelResource):
    
    thumb_default_size = "100x100"
    thumb_size = "100x100"
    thumb_crop = 'center'
    thumb_quality = 99
    thumb_query_name = 'thumb_size'
    user_name = fields.CharField(attribute = 'user__username')
    user_avatar = fields.CharField(attribute = 'user__email')
    likers = fields.ListField()
    
    class Meta:
        queryset = Post.objects.all().order_by('-id')
        resource_name = 'post'
        allowed_methods = ['get']
        paginator_class = Paginator
        fields = ['id','image','like','text','url']

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(PostResource, self).apply_filters(request, applicable_filters)
        
        user_id = request.GET.get('user_id', None)
        filters = {}
        
        if user_id:
            filters.update(dict(user_id=user_id))

        return base_object_list.filter(**filters).distinct()
    
    def dispatch(self, request_type, request, **kwargs):
        self.thumb_size = request.GET.get(self.thumb_query_name, self.thumb_default_size)        
        return super(PostResource, self).dispatch(request_type, request, **kwargs)
    
    def dehydrate(self, bundle):
        id = bundle.data['id']
        o_image = bundle.data['image']
        im = get_thumbnail(o_image, self.thumb_size, quality=self.thumb_quality)
        bundle.data['thumbnail'] = im
        bundle.data['hw'] = "%sx%s" % (im.height, im.width) 
        bundle.data['permalink'] = '/pin/%d/' % (int(id))
        
        user_email = bundle.data['user_avatar']
        bundle.data['user_avatar'] = daddy_avatar.daddy_avatar(user_email)
        
        likers = Likes.objects.filter(post_id=id).all()
        ar = []
        for lk in likers:
            ar.append([lk.user.id,lk.user.username, daddy_avatar.daddy_avatar(lk.user.email)])

        bundle.data['likers'] = ar
        
        if self.get_resource_uri(bundle) == bundle.request.path:
            # this is detail
            #del(bundle.data['thumbnail'])
                   
            img_path = os.path.join(settings.MEDIA_ROOT, o_image)
            print img_path
            im = Image.open(img_path)
            w,h = im.size
            bundle.data['hw'] = "%sx%s" % ( h,w )
        
        return bundle
