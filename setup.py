# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup


classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-shares',
    version='0.0.1',
    description='Object sharing for django',
    author='Troy Grosfield',
    maintainer='Troy Grosfield',
    long_description=README,
    url='https://github.com/infoagetech/django-shares',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'django >= 1.5.5',
    ],
    classifiers=classifiers
)
