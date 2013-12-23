from django_core.models.query import SafeDeleteQuerySet


class SharedObjectSafeDeleteQuerySet(SafeDeleteQuerySet):
    """QuerySet for SharedObjects when you don't want delete to necessarily
    remove the object from the database.  This works to set all object
    "is_deleted" fields to True.
    """

    def delete_safe(self, **kwargs):
        super(SharedObjectSafeDeleteQuerySet, self).delete_safe(**kwargs)

        ShareModel = self.model._meta.get_field_by_name('shares')[0].parent_model

        if 'is_deleted' in ShareModel._meta.get_all_field_names():
            # Set all share is_deleted fields to True
            share_ids = self.values_list('shares__id', flat=True)
            ShareModel.objects.filter(id=share_ids).update(is_deleted=True,
                                                           **kwargs)
