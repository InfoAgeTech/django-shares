from django.db import models
from django_core.models.mixins.crud import AbstractSafeDeleteModelMixin

from ..managers import SharedObjectManager


class AbstractSharedObject(models.Model):
    """Model mixin that represents a shared object.

    shares field should be overridded in the comsuming model if a different
    share class is being used.
    """
    objects = SharedObjectManager()

    class Meta:
        abstract = True

    @property
    def shares(self):
        """This must be overrided to user a related manager.  If not, this
        will throw a NotImplementedError.  Something like:

        class ConsumingModel(AbstractSharedObject):
            shares = generic.GenericRelation(Share)

        """
        raise NotImplementedError('Model "{0}" extends AbstractSharedObject '
                        'must explicitly defined a "shares" field in the '
                        'comsuming model. Something like \n\n'
                        'class ConsumingModel(AbstractSharedObject):\n'
                        '    shares = generic.GenericRelation(Share)'.format(
                                                             self.__class__))

    def get_share_class(self):
        """Gets the class instance associated to the "shares" model field."""
        return self.shares.model


class AbstractSharedObjectSafeDeleteModelMixin(AbstractSharedObject,
                                               AbstractSafeDeleteModelMixin):
    """Model mixin for safe deleting shares to an object."""

    class Meta:
        abstract = True

    def delete_safe(self, **kwargs):
        """Handles the deleting of an object.  Sets

        """
        super(AbstractSharedObjectSafeDeleteModelMixin,
              self).delete_safe(**kwargs)

        if hasattr(self, 'shares'):
            self.shares.all().delete_safe()

