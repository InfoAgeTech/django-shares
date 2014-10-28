from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django_core.db.models import BaseManager
from django_core.db.models import CommonManager
from django_core.db.models import TokenManager

from ...constants import Status


class ShareManager(CommonManager, TokenManager):

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
        content_type = (self.content_type
                        if hasattr(self, 'content_type') else None)

        if shared_object is None and hasattr(self, 'instance'):
            shared_object = self.instance

        if not kwargs:
            kwargs = {}

        kwargs.update({'created_user': created_user,
                       'last_modified_user': created_user,
                       'status': status})

        if not content_type:
            content_type = ContentType.objects.get_for_model(
                model=shared_object)

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

    def create_many(self, objs, for_user, created_user, status=Status.PENDING,
                    **kwargs):
        """Creates many shares at once of the same object type.  This is
        different from ``bulk_create`` because this can create many shares
        from many different objects of the same content type. For example,

        >> obj_1 = SomeObject.objects.create(...)
        >> obj_2 = SomeObject.objects.create(...)
        >> obj_3 = SomeObject.objects.create(...)
        >> objs = [obj_1, obj_2, obj_3]
        >> # This creates 3 shares (obj_1, obj_2, obj_3) for "some_user" that
        >> # all have the same attributes (i.e. status=Status.ACCEPTED).
        >> ShareManager.objects.create_many(objs=objs,
        ..                                  for_user=some_user,
        ..                                  status=Status.ACCEPTED)

        Under the covers this method calls ``bulk_create``.

        This should be called from a class and not a class instance.

        This method protects against duplicate shares for a single user.
        If a user is already sharing an object and another share for the same
        user is passed in ``obj``, no new share will be created.

        :param objs: iterable of objects to create shares for.  These objects
            MUST all be for the same object type!
        :param for_user: the user the shares are for
        :param created_user: the users creating all the shares
        """
        if not objs:
            return

        obj_ids = [obj.id for obj in objs]
        content_type = ContentType.objects.get_for_model(objs[0])
        current_obj_user_shares = self.model.objects.filter(
            for_user=for_user,
            object_id__in=obj_ids,
            content_type=content_type
        ).values_list('object_id', flat=True)

        shares = [self.model(for_user=for_user,
                             shared_object=obj,
                             status=status,
                             created_user=created_user,
                             **kwargs)
                  for obj in objs if obj.id not in current_obj_user_shares]

        self.model.save_prep(shares)
        # Don't want to call self.bulk_create here because I don't want the
        # instance associated with the shares since it will be different for
        # each share.
        return super(ShareManager, self).bulk_create(objs=shares, **kwargs)

    def bulk_create(self, shares, *args, **kwargs):
        """Bulk create's shares for object.

        This method also protects from users having duplicate shares to an
        object when this method is called from an instance of a class.  So, if
        a share is for a user who already has a share to the shared object,
        that share will not be added in the bulk_create.

        :param shares: iterable of share objects.
        """
        if not shares:
            return

        if hasattr(self, 'instance') and hasattr(self.instance, 'shares'):
            current_share_users = [s.for_user
                                   for s in self.instance.shares.all()
                                   if s.for_user]
            shares = [s for s in shares
                      if s.for_user not in current_share_users]

            for share in shares:
                # TODO: does this need to check for type?  Is this the
                #       correct behavior?
                if not share.shared_object:
                    share.shared_object = self.instance

        return super(ShareManager, self).bulk_create(objs=shares, *args,
                                                     **kwargs)

    def get_for_user(self, user, **kwargs):
        """Gets a shared objects for user."""
        if not user.is_authenticated():
            return None

        # TODO: could optimize this to first look and see if the shares have
        #       already been prefetched.  If so, do the loop, it not don't make
        #       the call to pull back all the shares.
        if hasattr(self, 'instance') and hasattr(self.instance, 'shares'):
            for share in self.instance.shares.all():
                if share.for_user_id == user.id:
                    return share

        queryset = self.filter(for_user=user, **kwargs)

        # If there isn't an ``instance`` then this was not called from an
        # instance of an object so all shares for a user will be returned.
        if not hasattr(self, 'instance'):
            return queryset

        try:
            # This is being called from an object instance and since a user
            # can only have 1 share per user, return that share.
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
            returned.  Otherwise, can be one of django_shares.constants.Status
            values.
        """
        if status is not None:
            kwargs['shares__status'] = status

        return self.filter(shares__for_user=for_user, **kwargs)
