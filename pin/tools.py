import os
import time
from datetime import datetime

from django.conf import settings

def create_filename(filename):
    
    d = datetime.now()
    folder = "%d/%d" % (d.year, d.month)
    
    paths = []
    paths.append("%s/pin/temp/o/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/temp/t/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/images/o/" % (settings.MEDIA_ROOT))
    paths.append("%s/pin/images/t/" % (settings.MEDIA_ROOT))
    
    for path in paths:
        abs_path = "%s%s" %(path, folder)
    
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        
    filestr = "%s/%f" % (folder, time.time())
    filestr = filestr.replace('.', '')
        
    filename = "%s%s" % (filestr, os.path.splitext(filename)[1])
    return filename