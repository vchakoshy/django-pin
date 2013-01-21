django-pin
==========

django pinterest like apllication 

Installation
------------

To install::
    
    pip install django-pip
    
Then add ``pin`` to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = (
        ...
        'pin',
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
