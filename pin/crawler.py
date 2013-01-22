import httplib
import lxml.html
import socket
import urllib2
import urlparse

from urllib2 import URLError, HTTPError

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

socket.setdefaulttimeout(10)

def get_url_content(url):
    try:
        f = urllib2.urlopen(url)
        content = f.read()
        return content
    except HTTPError:
        return 0
    except URLError:
        return 0
    except ValueError:
        return 0
    
    return 0

def check_content_type(url):
    #try:
        o=urlparse.urlparse(url)
        
        conn = httplib.HTTPConnection(o.netloc)
        conn.request("HEAD", o.path)
        res = conn.getresponse()
    
        content_type = res.getheader('content-type')
        if content_type.startswith('image'):
            return 'image'
        else:
            return 'text'
    #except:
        return 'text'

def validate_url(url):
    valid_url = URLValidator(verify_exists=False)
    
    try:
        valid_url(url)
    except ValidationError:
        return 0
    
    return 1

def get_images(url):
    if validate_url(url):
        images = []
        if check_content_type(url) == 'image':
            images.append(url)
        else:
            content = get_url_content(url)
            if content == 0:
                return 0
            tree = lxml.html.fromstring(content)
            
            for image in tree.xpath("//img/@src"):
                if not image.startswith('http://'):
                    image = urlparse.urljoin(url, image)
                
                if image not in images:
                    images.append(image)
            
        return images
    return 0