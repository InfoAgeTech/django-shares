from django.db import models
from django_core.models.mixins.crud import AbstractSafeDeleteModelMixin

from ..constants import Status
from ..managers import SharedObjectManager


class AbstractSharedObjectModelMixin(models.Model):
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


class SafeDeleteShareModelMixin(models.Model):
    """Model mixin for safe deleting an object where the status is set to
    DELETED and the object is not removed from the database.
    """

    class Meta:
        abstract = True

    def delete_safe(self):
        """Sets the status to DELETED."""
        self.status = Status.DELETED
        self.save()


class AbstractSafeDeleteSharedObjectModelMixin(AbstractSafeDeleteModelMixin):
    """Model mixin for safe deleting an object where the is_deleted field is
    set to True and the object is not removed from the database.

    The shares associated with the shared object have their status set to
    DELETED as well.
    """

    class Meta:
        abstract = True

    def delete_safe(self):
        super(AbstractSafeDeleteSharedObjectModelMixin, self).delete_safe()
        # Update status to all shares for this object
        self.shares.all().update(status=Status.DELETED)
