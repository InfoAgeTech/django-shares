from __future__ import unicode_literals


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
