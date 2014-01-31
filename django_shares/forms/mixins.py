from __future__ import unicode_literals


class SharedObjectFormMixin(object):
    """Form mixin for a shared object."""

    shared_object = None

    def __init__(self, shared_object=None, *args, **kwargs):
        self.shared_object = shared_object
        super(SharedObjectFormMixin, self).__init__(*args, **kwargs)
