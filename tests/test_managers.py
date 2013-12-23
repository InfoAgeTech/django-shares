from django.test.testcases import TestCase
from python_tools.random_utils import random_alphanum

from tests.test_models.models import TestSharedObjectSafeDeleteModel


class SharedObjectManagerTestCase(TestCase):

    def test_shared_object_safe_delete(self):
        """Test shared object is not deleted from the database, but instead the
        field "is_deleted" is set to True.
        """
        group = random_alphanum()
        obj = TestSharedObjectSafeDeleteModel.objects.create(group=group)
        TestSharedObjectSafeDeleteModel.objects.filter(group=group).delete_safe()

        obj_db = TestSharedObjectSafeDeleteModel.objects.get(id=obj.id)
        self.assertTrue(obj_db.is_deleted)

    def test_shared_object_safe_delete_false(self):
        """Test shared object is properly deleted depending of if the removal
        of the object is wanted or if the is_delete attribute is set to True.
        """
        group = random_alphanum()
        obj = TestSharedObjectSafeDeleteModel.objects.create(group=group)
        TestSharedObjectSafeDeleteModel.objects.filter(group=group).delete()

        with self.assertRaises(TestSharedObjectSafeDeleteModel.DoesNotExist):
            TestSharedObjectSafeDeleteModel.objects.get(id=obj.id)
