# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query_utils import Q


class ShareManager(models.Manager):
    """Manager for sharing objects."""

    def get_for_user(self, user):
        """Gets a shared objects for user."""
        return self.filter(for_user=user)

    def get_for_user_id(self, user_id):
        """Gets a shared objects for a user by user id."""
        return self.filter(for_user_id=user_id)

    def get_by_email(self, email):
        """Gets shares by an email."""
        return self.filter(Q(email=email) | Q(for_user__email=email))

    def get_by_token(self, token):
        """Gets a pending share by token."""
        try:
            return self.get(token=token)
        except self.model.DoesNotExist:
            return None

    def get_by_shared_object(self, obj):
        """Gets all shares for an object.
        
        :param obj: object to get shares for.
        """
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.id)
