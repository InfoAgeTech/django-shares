from django.contrib.contenttypes import generic
from django.db import models
from django_sharing.managers import SharedObjectManager
from django_sharing.managers import SharedObjectSafeDeleteManager
from django_sharing.mixins.models import AbstractSharedObject
from django_sharing.mixins.models import AbstractSharedObjectSafeDeleteModelMixin


class TestSharedObjectModel(AbstractSharedObject):
    """Test model for Shared objects."""
    group = models.CharField(max_length=50, blank=True, null=True)
    shares = generic.GenericRelation('django_sharing.Share')
    objects = SharedObjectManager()


class TestSharedObjectSafeDeleteModel(AbstractSharedObjectSafeDeleteModelMixin):
    """Test model for Shared objects with Safe delete functionality."""
    group = models.CharField(max_length=50, blank=True, null=True)
    shares = generic.GenericRelation('django_sharing.Share')
    objects = SharedObjectSafeDeleteManager()
