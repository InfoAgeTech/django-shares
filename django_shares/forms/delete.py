from django import forms


class SharedObjectRemoveShareForm(forms.Form):
    """Base form for shared object share.  Works as a placeholder when doing
    this like removing a share (delete view) and no fields are necessary.
    """
