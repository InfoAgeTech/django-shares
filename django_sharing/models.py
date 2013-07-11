# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_core.models import AbstractBaseModel
from python_tools.list_utils import make_obj_list

from .constants import Status
from .managers import ShareManager

User = get_user_model()


class AbstractShare(AbstractBaseModel):
    """Abstract Base share object represents basic shared information for a 
    specific user sharing an object.
    
    Fields:
    * for_user: the user the object is shared with.
    * email: email of the user who the share was sent to if user is unknown.
    * first_name: first name of the person invited
    * last_name: last name of the person invited
    * last_sent: date time the share was last sent.
    * created_user_id: the id of the user who sent the pending share
    * for_user_id: user_id the pending share is for (optional since they might  
        not be an actual user yet).
    * message: message sent to user in email.
    * content_type: the content type of the generic shared object
    * object_id: the object id of the shared object
    * shared_object: the object being shared.
    * token: share token. 
    
    """
    for_user = models.ForeignKey(User, blank=True, null=True, related_name='+')
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    last_sent = models.DateTimeField(default=datetime.utcnow)
    message = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=50, db_index=True, unique=True)
    status = models.CharField(max_length=25,
                              default=Status.PENDING,
                              choices=Status.CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    shared_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = ShareManager()

    class Meta:
        abstract = True

    @classmethod
    def save_prep(cls, instance_or_instances):
        """Preprocess the object before the object is saved.  This automatically 
        gets called when the save method gets called.
        """
        instances = make_obj_list(instance_or_instances)

        for instance in instances:
            if not instance.token:
                instance.token = instance.__class__.objects.get_next_token()

        return super(AbstractShare, cls).save_prep(instance_or_instances=instances)

    def accept(self, **kwargs):
        """Accept a share by updating the status to accepted.
        
        :param kwargs: additional fields that needs to be updated when the 
            field is accepted.
        """
        self.status = Status.ACCEPTED

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        return self.save()

    def decline(self, **kwargs):
        """Accept a share by updating the status to accepted.
        
        :param kwargs: additional fields that needs to be updated when the 
            field is accepted.
        """
        self.status = Status.DECLINED

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        return self.save()

    def copy(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []

        if 'token' not in exclude_fields:
            # Token should be unique thus removed when making a copy of a share
            # object.
            exclude_fields.append('token')

        return super(AbstractShare, self).copy(exclude_fields=exclude_fields)


class Share(AbstractShare):
    """The implementation for a shared object."""

    class Meta:
        ordering = ['-created_dttm']
        # Make sure you can only have 1 share per user per shared_object
        unique_together = ('content_type', 'object_id', 'for_user',)
        index_together = [
            ['content_type', 'object_id'],
        ]
