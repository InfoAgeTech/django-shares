"""
Module all about url shares based on url keyword arg.
"""
from __future__ import unicode_literals

from django.views.generic.edit import DeleteView

from ..forms import SharedObjectRemoveShareForm


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
        if self.url_share is None:
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
