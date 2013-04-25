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
    * for_user: the user the object is shared with.
    * email: email of the user who the share was sent to if user is unknown.
    * first_name: first name of the person invited
    * last_name: last name of the person invited
    * last_sent: date time the share was last sent.
    * created_id: the id of the user who sent the pending share
    * for_user_id: user_id the pending share is for (optional since they might  
        not be an actual user yet).
    * message: message sent to user in email.
    * content_type: the content type of the generic shared object
    * object_id: the object id of the shared object
    * shared_object: the object being shared.
    * token: pending share token key. 
    
    """
    for_user = models.ForeignKey(User, blank=True, null=True, related_name='+')
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_sent = models.DateTimeField(default=datetime.utcnow)
    message = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=50, db_index=True, unique=True)
    status = models.CharField(max_length=25, choices=Status.CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    shared_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = ShareManager()

    class Meta:
        ordering = ['-created_dttm']
        # Make sure you can only have 1 share per user per shared_object
        unique_together = ('content_type', 'object_id', 'for_user',)
        index_together = [
            ['content_type', 'object_id'],
        ]

    def save(self, *args, **kwargs):

        if not self.token:
            self.token = random_alphanum_id(id_len=25)

        return super(Share, self).save(*args, **kwargs)

    @classmethod
    def add_for_user(cls, created_by_user, for_user, shared_object,
                     status=Status.PENDING, **kwargs):
        """Adds a share for an existing user.
        
        :param created_by_user: the user creating the share.
        :param for_user: the user the shared object is being shared with.
        :param shared_object: the object being shared.
        :param status: the status of the shared object.
        :param kwargs: can be any keyword args on the sharing model.
        """
        share = cls(created=created_by_user,
                    last_modified=created_by_user,
                    for_user=for_user,
                    shared_object=shared_object,
                    status=status,
                    **kwargs)
        share.save()
        return share

    @classmethod
    def add_for_non_user(cls, created_by_user, shared_object, email, first_name,
                         last_name, message=None, status=Status.PENDING,
                         **kwargs):
        """Adds a share for a user who potentially isn't a member of the site
        yet.
        
        :param created_by_user: the user creating the share.
        :param shared_object: the object being shared.
        :param email: email of the person being shared with.
        :param first_name: first name of the person being shared with.
        :param last_name: last name of the person being shared with.
        :param message: message to the user being shared with
        :param status: the status of the shared object. Since this user isn't
            necessarily a site user yet.
        """
        share = cls(created=created_by_user,
                    last_modified=created_by_user,
                    shared_object=shared_object,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    message=message,
                    status=status,
                    **kwargs)
        share.save()
        return share
