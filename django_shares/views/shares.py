from __future__ import unicode_literals

from ..constants import Status
from ..utils import sort_shares_by_status


class SharedObjectUserShareViewMixin(object):
    """View mixin for the auth user's object share. The shared object is
    assumed to be the object returned from `get_object` call from anything that
    subclasses django.views.generic.detail.SingleObjectMixin
    """
    shared_object_user_share = None  # auth user's share for this object

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            user_share = self.get_shared_object().shares.get_for_user(
                self.request.user
            )
            self.shared_object_user_share = user_share

        return super(SharedObjectUserShareViewMixin,
                     self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedObjectUserShareViewMixin,
                        self).get_context_data(**kwargs)
        context['shared_object_user_share'] = self.shared_object_user_share
        return context


class SharedObjectSharesViewMixin(SharedObjectUserShareViewMixin):
    """View mixin for a shared object.  The shared object is assumed to be
    the object returned from `get_object` call from anything that subclasses
    django.views.generic.detail.SingleObjectMixin
    """
    shared_object_shares_accepted = None
    shared_object_shares_pending = None
    shared_object_shares_declined = None
    shared_object_shares_inactive = None
    shared_object_shares_deleted = None

    def dispatch(self, *args, **kwargs):
        self.set_sharing_for_object(obj=self.get_shared_object(),
                                    attr_prefix='shared_object')
        return super(SharedObjectSharesViewMixin,
                     self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedObjectSharesViewMixin,
                        self).get_context_data(**kwargs)

        for status in Status.get_keys():
            attr_name = u'shared_object_shares_{0}'.format(status.lower())
            context[attr_name] = getattr(self, attr_name, []) or []

        return context

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
            setattr(self, u'{0}_shares_inactive'.format(attr_prefix),
                    self.shared_object_shares_inactive)
            setattr(self, u'{0}_shares_deleted'.format(attr_prefix),
                    self.shared_object_shares_deleted)
            return

        shares = obj.shares.all().prefetch_related('for_user',
                                                   'created_user',
                                                   'shared_object')

        shares_by_status = sort_shares_by_status(shares=shares)

        for status in Status.get_keys():
            attr_name = u'{0}_shares_{1}'.format(attr_prefix, status.lower())
            setattr(self,
                    attr_name,
                    shares_by_status.get(status, []))
