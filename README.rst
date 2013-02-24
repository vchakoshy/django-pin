django-pin
==========

django pinterest like apllication 

Installation
------------

Requirements::

    pip install -r requirements.txt

To install::
    
    pip install django-pin
    
Then add ``pin`` to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = (
        ...
        'pin',
        'django.contrib.comments',
        'django.contrib.humanize',
        'django.contrib.flatpages',
        'daddy_avatar',
        'sorl.thumbnail',
        'taggit',
        'compressor',
        ...
    )

In your urls.py:

.. code:: python

    urlpatterns = patterns('',
        url(r'pin/', include('pin.urls')),

        # other urls ...
    )


Live demo
---------

    http://www.wisgoon.com/pin/

    http://www.shiastock.com/
