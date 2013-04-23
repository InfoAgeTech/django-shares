# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_tools.models import AbstractBaseModel
import datetime

User = get_user_model()


class SharePending(AbstractBaseModel):
    """This is the base model used for pending requests. 
    
    When first created, the id and the token will be the same.  These are two
    separate fields because the id should never change.  The token could get 
    reassigned if it expires or a new token needs to be generated at a later 
    time.
    
    Fields:
    
    * email: email of the user who the share was sent to if uid is unknown.
    * first_name: first name of the person invited
    * last_name: last name of the person invited
    * last_sent: date time the share was last sent.
    * created_id: the id of the user who sent the pending share
    * for_user_id: user_id the pending share is for (optional since they might  
        not be an actual user yet).
    * message: message sent to user in email.
    * token: pending share token key.
    
    """
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_sent = models.DateTimeField(default=datetime.datetime.utcnow)
#    for_user = models.ForeignKey(User, blank=True, null=True)
    message = models.TextField()
    token = models.CharField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # TODO: could add a JSONField here and allow this model to be extended
    #       and add additional properties to that field.  Then new fields would
    #       be accessed via
    #
    # _sharing_metadata = JSONField()
    #
    # @property
    # def some_attribute_name(self):
    #    self._sharing_metadata.get('some_attr_name')


class Share(AbstractBaseModel):
    """Base share object represents an embedded document of information for a 
    specific user sharing a document.
    
    Fields:
    
    * for_user_id = user id for sharing this instance. 
    
    """
    for_user = models.ForeignKey(User, blank=True, null=True)
    # TODO: Could use a second generic foreign key here to represent the metadata
    #       for whatever type of share it was.  So, it's a bill share I would have
    #       things like amount, percent share, etc on a SomeObjectShareMeta models which
    #       is what the generic key would reference.
    #
    # Or just create a separate model for SomeObjectShare and make this model abstract?
    #
    # See third option for a JSONField above (can't query off it's values)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
