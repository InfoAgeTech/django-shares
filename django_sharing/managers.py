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


class ShareManager(models.manager):
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
#
# class SharePendingManager(CommonShareManager):
#    """Manager for pending share object."""
#
#    def get_by_email(self, email):
#        return self.filter(email=email)
#
#    def get_by_token(self, token):
#        """Gets a pending share by token."""
#        try:
#            return self.get(token=token)
#        except self.model.DoesNotExist:
#            return None
