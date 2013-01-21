django-pin
==========

django pinterest like apllication 

Installation
------------

Requirements::

    django user profile ``pip install django-user-profile``
    django daddy avatar ``pip install django-daddy-avatar``
    sorl thumbnail      ``pip install sorl.thumbnail``

To install::
    
    pip install django-pin
    
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
