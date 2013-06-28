NOTE: This is not stable yet and will likely change!  Please don't use in production until the 1.0 release.

==============
django-sharing
==============
:Info: django-recurrence is a python recurrence module written for django.
:Repository: https://github.com/InfoAgeTech/django-sharing
:Author: Troy Grosfield (http://github.com/troygrosfield)
:Maintainer: Troy Grosfield (http://github.com/troygrosfield)

.. image:: https://travis-ci.org/InfoAgeTech/django-sharing.png?branch=master
  :target: http://travis-ci.org/InfoAgeTech/django-sharing

About
=====

Handles object sharing in django.  Don't clone.  Not stable.

Example
=======
Basic example:

    from django.contrib.contenttypes import generic
    from django.db import models
    from django_sharing.models import Share

    class Car(models.Model):
        """A model that will be shared."""
        # Add the reverse relation since the shared object is a generic object.
        shares = generic.GenericRelation(Share)


Extending the sharing model:

    from django.contrib.contenttypes import generic
    from django.db import models
    from django_sharing.models import Share

    class CarShare(Share):
        """Extending the share model to add additional attributes."""
        day = models.CharField(max_length=50)

    class Car(models.Model):
        """A model that will be shared."""
        # Add the reverse relation since the shared object is a generic object.
        shares = generic.GenericRelation(CarShare)


Running Tests
=============
    python manage.py test
