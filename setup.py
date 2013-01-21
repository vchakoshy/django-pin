from setuptools import find_packages

from distutils.core import setup


version = '1.1.0'

setup(
    name = "django-pin",
    version = version,
    author = "vahid chakoshy",
    author_email = "vchakoshy@gmail.com",
    description = "pinterest apllication like in Django",
    url = "http://www.wisgoon.com/",
    packages=find_packages(),
    include_package_data = True,
    zip_safe=False,
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
