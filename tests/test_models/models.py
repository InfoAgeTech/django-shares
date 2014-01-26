from django.contrib.contenttypes import generic
from django.db import models

from django_shares.managers import SharedObjectManager
from django_shares.mixins.models import AbstractSharedObjectModelMixin


class TestSharedObjectModel(AbstractSharedObjectModelMixin):
    """Test model for Shared objects."""
    group = models.CharField(max_length=50, blank=True, null=True)
    shares = generic.GenericRelation('django_shares.Share')
    objects = SharedObjectManager()
