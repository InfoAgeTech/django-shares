NOTE: This is not stable yet and will likely change!  Please don't use in production until the 1.0 release.

.. |travis-ci| image:: https://travis-ci.org/InfoAgeTech/django-shares.png?branch=master
    :target: http://travis-ci.org/InfoAgeTech/django-shares
    :alt: Travis CI
.. |coveralls| image:: https://coveralls.io/repos/InfoAgeTech/django-shares/badge.png
    :target: https://coveralls.io/r/InfoAgeTech/django-shares
    :alt: Code Coverage
.. |version| image:: https://badge.fury.io/py/django-shares.png
    :target: http://badge.fury.io/py/django-shares
    :alt: Version
.. |license| image:: https://pypip.in/license/django-shares/badge.png
    :target: https://github.com/InfoAgeTech/django-shares/blob/master/LICENSE
    :alt: MIT License

|travis-ci| |coveralls| |version| |license| | `Documentation <http://django-shares.readthedocs.org>`_

=============
django-shares
=============
django-shares is a python sharing module written for django that handles object sharing.  Don't clone.  Not stable.

Installation
============
Install from `pypi <https://pypi.python.org/pypi/django-shares>`_ via pip::

   pip install django-shares

Example
=======
Basic example::

    from django.contrib.contenttypes import generic
    from django.db import models
    from django_shares.models import Share

    class Car(models.Model):
        """A model that will be shared."""
        # Add the reverse relation since the shared object is a generic object.
        shares = generic.GenericRelation(Share)


Extending the sharing model::

    from django.contrib.contenttypes import generic
    from django.db import models
    from django_shares.models import AbstractShare

    class CarShare(AbstractShare):
        """Extending the share model to add additional attributes."""
        day = models.CharField(max_length=50)

    class Car(models.Model):
        """A model that will be shared."""
        # Add the reverse relation since the shared object is a generic object.
        shares = generic.GenericRelation(CarShare)


Running Tests
=============
From the tests directory where the manage.py file is, run the following command::

    python manage.py test
