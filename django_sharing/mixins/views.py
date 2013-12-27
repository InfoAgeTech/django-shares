# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from django_core.views.mixins.common import CommonSingleObjectViewMixin

from ..constants import Status
from ..utils import get_share_for_user
from ..utils import sort_shares_by_status
from .forms import SharedObjectRemoveShareForm


class SharedSingleObjectMixin(CommonSingleObjectViewMixin, SingleObjectMixin):
    """For use when you have a shared object in context.  Use this view mixin
    when the object viewing object is the the shared object.

    Attributes
    ==========
    * is_object_shared_object: boolean indicating if the shared object is the
        object that will be represented by the SingleObjectMixin.  This helps
        to check in cases where the shared object is different than the object
        for the view.  An example of this would be a view for a shared object's
        share.  In this case the share would be the `object` for the view to
        act on.

        This value is determined if self.shared_object_model != self.model
    """
    is_object_shared_object = False

    def dispatch(self, *args, **kwargs):
        self.set_object_defaults()
        self.shared_object = self.get_shared_object()

        if self.is_object_shared_object:
            self.object = self.shared_object
        elif not hasattr(self, 'object'):
            self.object = self.get_object()

        return super(SharedSingleObjectMixin, self).dispatch(*args, **kwargs)

    def set_object_defaults(self):
        """If shared_object* attributes aren't set on the view, then fall back
        to the SingleObjectMixin model attributes.
        """
        self.is_object_shared_object = self.model and self.shared_object_model

        if not self.model and self.shared_object_model:
            self.is_object_shared_object = True
            self.model = self.shared_object_model

        if not self.queryset and self.shared_object_queryset:
            self.queryset = self.shared_object_queryset

        if not self.pk_url_kwarg and self.shared_object_pk_url_kwarg:
            self.pk_url_kwarg = self.shared_object_pk_url_kwarg

        if (not self.context_object_name and
            self.shared_object_context_object_name):
            self.context_object_name = self.shared_object_context_object_name

    # TODO: This might be overkill and I'm not sure this method is needed.
    def get_object(self, **kwargs):
        if self.object:
            return self.object

        try:
            return super(SharedSingleObjectMixin, self).get_object(**kwargs)
        except:
            return self.shared_object


class SharedObjectViewMixin(object):
    """For use when you have a shared object in context."""

    shared_object = None  # the object being shared
    shared_object_model = None
    shared_object_queryset = None
    shared_object_pk_url_kwarg = None
    shared_object_context_object_name = None

    def dispatch(self, *args, **kwargs):
        self.shared_object = self.get_shared_object()
        return super(SharedObjectViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedObjectViewMixin,
                        self).get_context_data(**kwargs)
        context['shared_object'] = self.shared_object
        return context

    def get_shared_object(self):
        """Get the object that's being shared.  This can be overridden.
        Defaults to self.object.
        """
        return self.shared_object


class SharedObjectSharesViewMixin(object):
    """View mixin for a shared object.  The shared object is assumed to be
    the object returned from `get_object` call from anything that subclasses
    django.views.generic.detail.SingleObjectMixin
    """
    shared_object_user_share = None  # auth user's share for this object
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
        context['shared_object_user_share'] = self.shared_object_user_share

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
        setattr(self,
                u'{0}_user_share'.format(attr_prefix),
                get_share_for_user(shares=shares,
                                   user=self.request.user))

        for status in Status.get_keys():
            attr_name = u'{0}_shares_{1}'.format(attr_prefix, status.lower())
            setattr(self,
                    attr_name,
                    shares_by_status.get(status, []))


class SharedObjectUrlShareViewMixin(object):
    """Adds the shared object share from a pk in the url.

    This mixin puts the following attributes on the view:

    * url_share: the share for the shared object with the token provided by
        the 'token_url_kwarg'.
    """

    token_url_kwarg = 'token'
    url_share = None

    def dispatch(self, *args, **kwargs):
        self.url_share = self.get_url_share(**kwargs)
        return super(SharedObjectUrlShareViewMixin,
                     self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedObjectUrlShareViewMixin,
                        self).get_context_data(**kwargs)
        context['url_share'] = self.url_share
        return context

    def get_url_share(self, **kwargs):
        if self.url_share == None:
            self.url_share = self.get_shared_object().shares.get_by_token_or_404(
                                        token=kwargs.get(self.token_url_kwarg))

        return self.url_share


class SharedObjectShareViewMixin(SharedObjectUrlShareViewMixin):

    def get_object(self, **kwargs):
        return self.get_url_share(**kwargs)


class SharedObjectRemoveShareDeleteView(SharedObjectShareViewMixin,
                                        DeleteView):
    """Form view to remove a share from a shared object."""
    form_class = SharedObjectRemoveShareForm

    def delete(self, request, *args, **kwargs):
        self.url_share.last_modified_user = self.request.user
        return super(SharedObjectRemoveShareDeleteView,
                     self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.shared_object.get_absolute_url()


class ShareRequiredViewMixin(object):
    """Share mixin that ensures the authenticated user has a share to the
    object being viewed or get a permission denied.

    This method assumes the following mixin has already been called:

        * django_sharing.mixins.views.SharedObjectSharesViewMixin
    """
    def dispatch(self, *args, **kwargs):
        if not getattr(self, 'shared_object_user_share', None):
            raise PermissionDenied

        return super(ShareRequiredViewMixin, self).dispatch(*args, **kwargs)
