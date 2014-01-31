from django.core.exceptions import PermissionDenied


class ShareRequiredViewMixin(object):
    """Share mixin that ensures the authenticated user has a share to the
    object being viewed or get a permission denied.

    This method assumes the following mixin has already been called:

        * django_shares.mixins.views.SharedObjectSharesViewMixin
    """
    def dispatch(self, *args, **kwargs):
        if not getattr(self, 'shared_object_user_share', None):
            raise PermissionDenied

        return super(ShareRequiredViewMixin, self).dispatch(*args, **kwargs)
