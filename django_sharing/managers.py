# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django_core.managers import BaseManager
from django_core.managers import TokenManager

from .constants import Status


class ShareManager(TokenManager):
    """Manager for the object share. This manager is used for the share
    object (model) that either extends Share or implements AbstractShare.
    """

    def create_for_user(self, created_user, for_user, shared_object=None,
                        status=Status.PENDING, **kwargs):
        """Create a share for an existing user. This method ensures that only
        one share will be created per user. So a user can only have at most 1
        share to an object.

        :param created_user: the user creating the share.
        :param for_user: the user the shared object is being shared with.
        :param shared_object: the object being shared.
        :param status: the status of the shared object.
        :param kwargs: can be any keyword args on the sharing model.
        """
        if shared_object is None:
            shared_object = self.instance

        if not kwargs:
            kwargs = {}

        kwargs.update({'created_user': created_user,
                       'last_modified_user': created_user,
                       'status': status})

        content_type = ContentType.objects.get_for_model(model=shared_object)
        return self.get_or_create(for_user=for_user,
                                  content_type=content_type,
                                  object_id=shared_object.id,
                                  defaults=kwargs)[0]

    def create_for_non_user(self, created_user, email, first_name, last_name,
                            shared_object=None, message=None,
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
        if shared_object is None:
            shared_object = self.instance

        return self.create(created_user=created_user,
                           last_modified_user=created_user,
                           shared_object=shared_object,
                           email=email,
                           first_name=first_name,
                           last_name=last_name,
                           message=message,
                           status=status,
                           **kwargs)

    def get_for_user(self, user, **kwargs):
        """Gets a shared objects for user."""
        queryset = self.filter(for_user=user, **kwargs)

        if not hasattr(self, 'instance'):
            return queryset

        try:
            return queryset.get()
        except:
            return None

    def get_for_user_id(self, user_id, **kwargs):
        """Gets a shared objects for a user by user id."""
        return self.filter(for_user_id=user_id, **kwargs)

    def get_by_email(self, email, **kwargs):
        """Gets shares by an email."""
        # TODO: To lower()?
        queryset = self.filter(Q(email=email) | Q(for_user__email=email),
                               **kwargs)

        if not hasattr(self, 'instance'):
            return queryset

        try:
            return queryset.get()
        except:
            return None

    def get_by_shared_object(self, obj, **kwargs):
        """Gets all shares for an object.

        :param obj: object to get shares for.
        """
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.id,
                           **kwargs)


class SharedObjectManager(BaseManager):
    """Manager for the object being shared.  This likely means you have some
    type of relation to shared objects.  The models will likely have something
    like:

    shares = generic.GenericRelation(SomeShare)

    Note: this manager assumes you're calling the shares "shares".
    """

    def get_for_user(self, for_user, status=None, **kwargs):
        """Get objects that are being shared with this user.

        :param for_user: the user to get the objects for.
        :param status: status of the share.  If None, all status' will be
            returned.  Otherwise, can be one of django_sharing.constants.Status
            values.
        """
        if status is not None:
            kwargs['shares__status'] = status

        return self.filter(shares__for_user=for_user, **kwargs)
