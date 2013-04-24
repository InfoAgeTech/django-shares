# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_sharing.constants import Status
from django_sharing.managers import ShareManager
from django_tools.models import AbstractBaseModel
from python_tools.random_utils import random_alphanum_id

User = get_user_model()


class Share(AbstractBaseModel):
    """Base share object represents an embedded document of information for a 
    specific user sharing a document.
    
    Fields:
    
    * email: email of the user who the share was sent to if user is unknown.
    * first_name: first name of the person invited
    * last_name: last name of the person invited
    * last_sent: date time the share was last sent.
    * created_id: the id of the user who sent the pending share
    * for_user_id: user_id the pending share is for (optional since they might  
        not be an actual user yet).
    * message: message sent to user in email.
    * token: pending share token key. 
    
    """
    for_user = models.ForeignKey(User, blank=True, null=True, related_name='+')
    # START for pending shares
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_sent = models.DateTimeField(default=datetime.utcnow)
    message = models.TextField()
    # END for pending shares... create a separata object for this?
    token = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=25, choices=Status.CHOICES)

    # TODO: Could use a second generic foreign key here to represent the metadata
    #       for whatever type of share it was.  So, it's a bill share I would have
    #       things like amount, percent share, etc on a SomeObjectShareMeta models which
    #       is what the generic key would reference.
    #
    #       DON'T do the above! What will happen behind the scenes is a join. If
    #       that's the case then i would be smarter to just create this as a model
    #       and extend it will another model (neither would be ebstract).
    #
    # Or just create a separate model for SomeObjectShare and make this model abstract?
    #
    # If this model is abstract, then I shouldn't need a generic foreign key below
    # I should just add the actual foreign key this object is for.
    #
    # If I do a generic foreign key I could do proxy models that references this
    # model. However, that still doesn't resolve needing extra fields.
    #
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = ShareManager()

    class Meta:
        ordering = ['-created_dttm']

    def save(self, *args, **kwargs):

        if not self.token:
            self.token = random_alphanum_id(id_len=25)

        return super(Share, self).save(*args, **kwargs)

    @classmethod
    def add_for_user(cls, user, status=Status.PENDING, **kwargs):
        """Adds a share for an existing user."""
        share = cls(for_user=user, **kwargs)
        share.save()
        return share

    @classmethod
    def add_for_non_user(cls, email, first_name, last_name, message=None,
                         status=Status.PENDING, **kwargs):
        """Adds a share for a user who potentially isn't a member of the site
        yet.
        """
        share = cls(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    message=message,
                    status=status,
                    **kwargs)
        share.save()
        return share


# class AbstractSharePending(AbstractBaseModel):
#    """This is the base model used for pending requests.
#
#    When first created, the id and the token will be the same.  These are two
#    separate fields because the id should never change.  The token could get
#    reassigned if it expires or a new token needs to be generated at a later
#    time.
#
#    Fields:
#
#    * email: email of the user who the share was sent to if uid is unknown.
#    * first_name: first name of the person invited
#    * last_name: last name of the person invited
#    * last_sent: date time the share was last sent.
#    * created_id: the id of the user who sent the pending share
#    * for_user_id: user_id the pending share is for (optional since they might
#        not be an actual user yet).
#    * message: message sent to user in email.
#    * token: pending share token key.
#
#    """
#    email = models.EmailField()
#    first_name = models.CharField(max_length=100)
#    last_name = models.CharField(max_length=100)
#    last_sent = models.DateTimeField(default=datetime.utcnow)
#    for_user = models.ForeignKey(User, blank=True, null=True)
#    message = models.TextField()
#    token = models.CharField(max_length=50, unique=True)
#    objects = SharePendingManager()
# #    content_type = models.ForeignKey(ContentType)
# #    object_id = models.PositiveIntegerField()
# #    content_object = generic.GenericForeignKey('content_type', 'object_id')
#
#    # TODO: could add a JSONField here and allow this model to be extended
#    #       and add additional properties to that field.  Then new fields would
#    #       be accessed via
#    #
#    # _sharing_metadata = JSONField()
#    #
#    # @property
#    # def some_attribute_name(self):
#    #    self._sharing_metadata.get('some_attr_name')
#
#    class Meta:
#        abstract = True
