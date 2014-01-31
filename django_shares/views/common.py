from __future__ import unicode_literals

from django.views.generic.detail import SingleObjectMixin
from django_core.views import CommonSingleObjectViewMixin


class SharedSingleObjectMixin(CommonSingleObjectViewMixin, SingleObjectMixin):
    """For use when you have a shared object in context.  Use this view mixin
    when the object viewing object is the the shared object.

    Attributes:

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