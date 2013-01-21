from tastypie.resources import ModelResource
from tastypie.paginator import Paginator

from sorl.thumbnail import get_thumbnail
from pin.models import Post

class PostResource(ModelResource):
    
    thumb_default_size = "100x100"
    thumb_size = "100x100"
    thumb_crop = 'center'
    thumb_quality = 99
    thumb_query_name = 'thumb_size'
    
    class Meta:
        queryset = Post.objects.all().order_by('-id')
        resource_name = 'post'
        allowed_methods = ['get']
        paginator_class = Paginator
        
    def dispatch(self, request_type, request, **kwargs):
        self.thumb_size = request.GET.get(self.thumb_query_name, self.thumb_default_size)        
        return super(PostResource, self).dispatch(request_type, request, **kwargs)

    def dehydrate(self, bundle):
        id = bundle.data['id']
        o_image = bundle.data['image']
        im = get_thumbnail(o_image, self.thumb_size, crop=self.thumb_crop, quality=self.thumb_quality)
        bundle.data['thumbnail'] = im
        bundle.data['permalink'] = '/pin/%d/' % (int(id))
        
        return bundle
