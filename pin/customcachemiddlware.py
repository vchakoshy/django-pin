from django.middleware.cache import *
import re

from django.conf import settings

class CustomFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    """
    Implements a custom version of the process_request 
    function of django's FetchFromCacheMiddleware
    
    Used in conjunction with uwsgi's cache backend:
        http://projects.unbit.it/uwsgi/wiki/CachingFramework

    Heavily influence by this write-up: 
        http://soyrex.com/articles/django-nginx-memcached/
    """
    def process_request(self, request):
        """
        Checks whether the page is already cached and returns the cached
        version if available.
        """

        if not request.method in ('GET', 'HEAD'):
            request._cache_update_cache = False
            return None # Don't bother checking the cache.
        
        """
        see if current request url "is" 
        in the list of urls to bypass in the cache
        if so, don't check the cance
        """
        for regex in settings.CACHE_BYPASS_URLS:
            request_url = request.get_full_path()
            if re.match(regex, request_url):
                request._cache_update_cache = False
                return None

        # try and get the cached GET response
        cache_key = get_cache_key(request, self.key_prefix, 'GET', cache=self.cache)

        if cache_key is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.
        response = self.cache.get(cache_key, None)
        # if it wasn't found and we are looking for a HEAD, try looking just for that
        if response is None and request.method == 'HEAD':
            cache_key = get_cache_key(request, self.key_prefix, 'HEAD', cache=self.cache)
            response = self.cache.get(cache_key, None)

        if response is None:
            request._cache_update_cache = True
            return None # No cache information available, need to rebuild.

        # hit, return cached response
        request._cache_update_cache = False
        return response