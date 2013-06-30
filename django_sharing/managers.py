# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django_tools.managers import TokenManager

from .constants import Status


class ShareManager(TokenManager):
    """Manager for sharing objects."""

    def create_for_user(self, created_user, for_user, shared_object,
                        status=Status.PENDING, **kwargs):
        """Create a share for an existing user.
        
        :param created_user: the user creating the share.
        :param for_user: the user the shared object is being shared with.
        :param shared_object: the object being shared.
        :param status: the status of the shared object.
        :param kwargs: can be any keyword args on the sharing model.
        """
        return self.create(created_user=created_user,
                            last_modified_user=created_user,
                            for_user=for_user,
                            shared_object=shared_object,
                            status=status,
                            **kwargs)

    def create_for_non_user(self, created_user, shared_object, email,
                            first_name, last_name, message=None,
                            status=Status.PENDING, **kwargs):
        """Create a share for a user who potentially isn't a member of the site
        yet.
        
        :param created_user: the user creating the share.
        :param shared_object: the object being shared.
        :param email: email of the person being shared with.
        :param first_name: first name of the person being shared with.
        :param last_name: last name of the person being shared with.
        :param message: message to the user being shared with
        :param status: the status of the shared object. Since this user isn't
            necessarily a site user yet.
        """
        return self.create(created_user=created_user,
                           last_modified_user=created_user,
                           shared_object=shared_object,
                           email=email,
                           first_name=first_name,
                           last_name=last_name,
                           message=message,
                           status=status,
                           **kwargs)

    def get_for_user(self, user):
        """Gets a shared objects for user."""
        return self.filter(for_user=user)

    def get_for_user_id(self, user_id):
        """Gets a shared objects for a user by user id."""
        return self.filter(for_user_id=user_id)

    def get_by_email(self, email):
        """Gets shares by an email."""
        # TODO: To lower()?
        return self.filter(Q(email=email) | Q(for_user__email=email))

    def get_by_shared_object(self, obj):
        """Gets all shares for an object.
        
        :param obj: object to get shares for.
        """
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.id)
