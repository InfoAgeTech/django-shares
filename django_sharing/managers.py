# -*- coding: utf-8 -*-
from django.db import models


# class CommonShareManager(models.manager):
#    """Manager methods common to both sharing and pending share models."""
#
#    def get_for_user(self, user):
#        """Gets a shared objects for user."""
#        return self.filter(for_user=user)
#
#    def get_for_user_id(self, user_id):
#        """Gets a shared objects for a user by user id."""
#        return self.filter(for_user_id=user_id)


class ShareManager(models.Manager):
    """Manager for sharing objects."""

    def get_for_user(self, user):
        """Gets a shared objects for user."""
        return self.filter(for_user=user)

    def get_for_user_id(self, user_id):
        """Gets a shared objects for a user by user id."""
        return self.filter(for_user_id=user_id)

    def get_by_email(self, email):
        return self.filter(email=email)

    def get_by_token(self, token):
        """Gets a pending share by token."""
        try:
            return self.get(token=token)
        except self.model.DoesNotExist:
            return None

    def get_by_content_object(self, obj):
        """Gets all shares for an object.
        
        :param obj: object to get shares for.
        """
        # I don't actually think I can do this. Might instead have to do:
        # content_type = ContentType.objects.get_for_model(obj)
        # return self.filter(content_type=content_type, object_id=obj.id)
        # or
        # return self.filter(content_type__pk=content_type.id, object_id=obj.id)
        return self.filter(content_object=obj)
