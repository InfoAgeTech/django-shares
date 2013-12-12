# -*- coding: utf-8 -*-
from django import forms


class SharedObjectRemoveShareForm(forms.Form):
    """Form for removing a shared object share."""


class SharedObjectFormMixin(object):
    """Form mixin for a shared object."""

    shared_object = None

    def __init__(self, shared_object=None, *args, **kwargs):
        self.shared_object = shared_object
        super(SharedObjectFormMixin, self).__init__(*args, **kwargs)
