from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.db import models
from django_shares.db.models import AbstractSharedObjectModelMixin
from django_shares.db.models.managers import SharedObjectManager


class TestSharedObjectModel(AbstractSharedObjectModelMixin):
    """Test model for Shared objects."""
    group = models.CharField(max_length=50, blank=True, null=True)
    shares = generic.GenericRelation('django_shares.Share')
    objects = SharedObjectManager()


class TestSharedObjectModel2(AbstractSharedObjectModelMixin):
    """Test model for Shared objects."""
    group = models.CharField(max_length=50, blank=True, null=True)
    shares = generic.GenericRelation('django_shares.Share')
    objects = SharedObjectManager()
