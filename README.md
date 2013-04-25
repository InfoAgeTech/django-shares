django-sharing
==============

Handles object sharing in django.  Don't clone.  Not stable.

Running Tests
=============
python manage.py test


Example
=======

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