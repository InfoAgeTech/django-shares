NOTE: This is not stable yet and will likely change!  Please don't use in production until the 1.0 release.

.. |travisci| image:: https://travis-ci.org/InfoAgeTech/django-shares.png?branch=master
  :target: http://travis-ci.org/InfoAgeTech/django-shares
.. |coveralls| image:: https://coveralls.io/repos/InfoAgeTech/django-shares/badge.png
  :target: https://coveralls.io/r/InfoAgeTech/django-shares

====================================
django-shares |travisci| |coveralls|
====================================
django-shares is a python sharing module written for django that handles object sharing.  Don't clone.  Not stable.

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
