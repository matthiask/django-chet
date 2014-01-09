#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-chet',
    version=__import__('chet').__version__,
    description=(
        'django-chet, honoring the most photogenic Jazz musician ever'
        ' with nice photos.'),
    long_description=read('README.rst'),
    author='Matthias Kestenholz',
    author_email='mk@406.ch',
    url='https://github.com/matthiask/django-chet/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=[],
    ),
    package_data={
        '': ['*.html', '*.txt'],
        'chet': [
            'locale/*/*/*.*',
            # 'static/form_designer/*.*',
            # 'static/form_designer/*/*.*',
            'templates/*.*',
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*',
        ],
    },
    install_requires=[
        'Django>=1.4.2',
    ],
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
    ],
    zip_safe=False,
)
