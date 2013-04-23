# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

classifiers = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='django-sharing',
    version='0.0.1',
    description='Sharing for django',
    author='Troy Grosfield',
    author_email='troy.grosfield@gmail.com',
    url='https://github.com/troygrosfield/django-sharing',
    # license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
    setup_requires=[
        'mongoengine >= 0.7.9',
        'django-nose >= 1.1'
    ],
    classifiers=classifiers
)
