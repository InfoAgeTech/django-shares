# TODO: move this into the reusable sharing app and put on the object manager
#       so i can call .shares.get_by_status?
# -*- coding: utf-8 -*-
from ..constants import Status
from django_core.mixins.common import CommonSingleObjectMixin
from django.core.exceptions import PermissionDenied
from django_sharing.utils import sort_shares_by_status
from django_sharing.utils import get_share_for_user
from django.http.response import Http404


class BaseShareViewMixin(object):

    def set_sharing_for_object(self, obj, attr_prefix=None):
        """Sets the sharing on the view.

        :param obj: set the sharing attributes on the view for this object.
        :param attr_prefix: the prefix to append to the attributes.  If None,
            the prefix will default to the class name lower cased.

        The following attributes get set on the view:

        {obj class or attr_prefix}_share = # user share
        {obj class or attr_prefix}_shares_accepted # list of accepted shares
                                                   # for the shared object
        {obj class or attr_prefix}_shares_pending # list of pending shares
                                                  # for the shared object
        {obj class or attr_prefix}_shares_declined # list of declined shares
                                                   # for the shared object

        Example:

        self == some view

        >> self.set_sharing_for_object(obj=xyz, attr_prefix='some_object')
        self.some_object_share # user share
        self.some_object_shares_accepted # list of accepted shares for the
                                         # shared object
        self.some_object_shares_pending # list of pending shares for the
                                        # shared object
        self.some_object_shares_declined # list of declined shares for the
                                         # shared object
        """
        if not attr_prefix:
            attr_prefix = obj.__class__.lower()

        if (attr_prefix != 'shared_object' and
            hasattr(self, 'shared_object') and
            self.shared_object == obj):
            setattr(self, u'{0}_user_share'.format(attr_prefix),
                    self.shared_object_user_share)
            setattr(self, u'{0}_shares_accepted'.format(attr_prefix),
                    self.shared_object_shares_accepted)
            setattr(self, u'{0}_shares_pending'.format(attr_prefix),
                    self.shared_object_shares_pending)
            setattr(self, u'{0}_shares_declined'.format(attr_prefix),
                    self.shared_object_shares_declined)
            return

        shares = obj.shares.all().prefetch_related('for_user',
                                                   'created_user')

        shares_by_status = sort_shares_by_status(shares=shares)
        setattr(self,
                u'{0}_user_share'.format(attr_prefix),
                get_share_for_user(shares=shares,
                                   user=self.request.user))

        for status in (Status.ACCEPTED, Status.PENDING, Status.DECLINED):
            attr_name = u'{0}_shares_{1}'.format(attr_prefix, status.lower())
            setattr(self,
                    attr_name,
                    shares_by_status.get(status, []))


class SharedObjectViewMixin(BaseShareViewMixin, CommonSingleObjectMixin):
    """View mixin for a shared object.  The shared object is assumed to be
    the object returned from `get_object` call from anything that subclasses
    django.views.generic.detail.SingleObjectMixin
    """
    shared_object = None  # the object being shared
    shared_object_user_share = None  # auth user's share for this object
    shared_object_shares_accepted = None
    shared_object_shares_pending = None
    shared_object_shares_declined = None

    def dispatch(self, *args, **kwargs):
        self.shared_object = self.get_shared_object()
        self.set_sharing_for_object(obj=self.shared_object,
                                    attr_prefix='shared_object')
        return super(SharedObjectViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedObjectViewMixin, self).get_context_data(**kwargs)
        context['shared_object'] = self.shared_object
        context['shared_object_user_share'] = self.shared_object_user_share

        for status in (Status.ACCEPTED, Status.PENDING, Status.DECLINED):
            attr_name = u'shared_object_shares_{0}'.format(status.lower())
            context[attr_name] = getattr(self, attr_name, []) or []

        return context

    def get_shared_object(self):
        """Get the object that's being shared.  This can be overridden.
        Defaults to self.object.
        """
        return self.get_object()


class ShareRequiredViewMixin(object):
    """Share mixin that ensures the authenticated user has a share to the
    object being viewed or get a permission denied.

    This method assumes the following mixin has already been called:

        * django_sharing.mixins.views.SharedObjectViewMixin
    """
    def dispatch(self, *args, **kwargs):
        if not getattr(self, 'shared_object_user_share', None):
            raise PermissionDenied

        return super(ShareRequiredViewMixin, self).dispatch(*args, **kwargs)


class CreatorRequiredViewMixin(CommonSingleObjectMixin):
    """Mixin that requires the self.object be created by the authenticated
    user.
    """
    def dispatch(self, request, *args, **kwargs):
        # does self.object exist at this point?
        share_obj = self.get_object()

        if not share_obj:
            raise Http404

        if share_obj.created_user_id != request.user.id:
            raise PermissionDenied

        return super(CreatorRequiredViewMixin, self).dispatch(request,
                                                              *args,
                                                              **kwargs)
