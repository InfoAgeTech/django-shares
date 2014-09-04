from __future__ import unicode_literals

from django_shares.constants import Status
from django_shares.models import Share
from django_testing.testcases.users import SingleUserTestCase
from django_testing.user_utils import create_user

from test_models.models import TestSharedObjectModel


class ShareTests(SingleUserTestCase):

    def setUp(self):
        """Run once per test."""
        super(ShareTests, self).setUp()
        self.shared_user = create_user()

    def tearDown(self):
        super(ShareTests, self).tearDown()
        self.shared_user.delete()

    def test_add_for_user(self):
        """Share a user object with a another user."""
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        self.assertEqual(share.shared_object, self.shared_user)

    def test_create_for_non_user(self):
        """Test for creating an object share with with an unknown user."""
        first_name = 'Jimmy'
        last_name = 'Buffet'
        email = 'hello@world.com'
        message = 'Share with me.'
        status = Status.PENDING
        share = Share.objects.create_for_non_user(created_user=self.user,
                                                  shared_object=self.shared_user,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  email=email,
                                                  message=message,
                                                  status=status)
        self.assertEqual(share.first_name, first_name)
        self.assertEqual(share.last_name, last_name)
        self.assertEqual(share.email, email)
        self.assertEqual(share.status, status)
        self.assertEqual(share.message, message)

    def test_get_for_user(self):
        """Get shares for user."""
        user = create_user()
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_for_user(user=user)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_for_user_id(self):
        """Get shares for a user id."""
        user = create_user()
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_for_user_id(user_id=user.id)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_email(self):
        """Get shares by email."""
        user = create_user()
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_by_email(email=user.email)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_by_token(self):
        """Get a share by token."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        share_db = Share.objects.get_by_token(token=share.token)

        self.assertEqual(share, share_db)

    def test_get_by_shared_object(self):
        """Get shares for a shared object."""
        shared_object = create_user()
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=shared_object)
        shares = Share.objects.get_by_shared_object(obj=shared_object)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_accept_share(self):
        """Test for accepting share."""
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        self.assertEqual(share.status, Status.PENDING)

        first_name = 'Test first name'
        share.accept(first_name=first_name)
        self.assertEqual(share.status, Status.ACCEPTED)
        self.assertEqual(share.first_name, first_name)

    def test_decline_share(self):
        """Test for accepting share."""
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)

        share.decline()
        self.assertEqual(share.status, Status.DECLINED)

    def test_inactivate(self):
        """Test for inactivating a share."""
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)

        share.inactivate()
        self.assertEqual(share.status, Status.INACTIVE)

    def test_is_accepted(self):
        """Test the is_accepted method."""
        share = Share(status=Status.ACCEPTED)
        self.assertTrue(share.is_accepted())

    def test_is_pending(self):
        """Test the is_pending method."""
        share = Share(status=Status.PENDING)
        self.assertTrue(share.is_pending())

    def test_is_declined(self):
        """Test the is_declined method."""
        share = Share(status=Status.DECLINED)
        self.assertTrue(share.is_declined())

    def test_copy(self):
        """Test for inactivating a share."""
        share = Share.objects.create_for_user(created_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)

        share_copy = share.copy()
        self.assertNotEqual(share.token, share_copy.token)

    def test_get_full_name_for_user(self):
        """Test get full name for a share for existing user."""
        first_name = 'John'
        last_name = 'Doe'
        user_2 = create_user(first_name=first_name, last_name=last_name)
        share = Share.objects.create_for_user(created_user=user_2,
                                              for_user=user_2,
                                              shared_object=self.shared_user)
        self.assertEqual(share.get_full_name(), '{0} {1}'.format(first_name,
                                                                 last_name))

    def test_get_full_name_for_non_user(self):
        """Test get full name for a share for non user."""
        first_name = 'John'
        last_name = 'Doe'
        share = Share.objects.create_for_non_user(created_user=self.user,
                                                email='test@test.com',
                                                first_name=first_name,
                                                last_name=last_name,
                                                shared_object=self.shared_user)
        self.assertEqual(share.get_full_name(), '{0} {1}'.format(first_name,
                                                                 last_name))

    def test_get_first_name(self):
        """Test get first name for a share."""
        first_name = 'John'
        share = Share(first_name=first_name)
        self.assertEqual(share.get_first_name(), first_name)

    def test_get_last_name(self):
        """Test get last name for a share."""
        last_name = 'Doe'
        share = Share(last_name=last_name)
        self.assertEqual(share.get_last_name(), last_name)

    def test_create_many(self):
        """Test for creating many objects at once.  This is different from
        bulk_create.  See ``create_many`` doc.
        """
        user = create_user()
        obj_1 = TestSharedObjectModel.objects.create()
        obj_2 = TestSharedObjectModel.objects.create()
        obj_3 = TestSharedObjectModel.objects.create()
        objs = [obj_1, obj_2, obj_3]
        # There shouldn't be any shares here.
        self.assertEqual(obj_1.shares.count(), 0)
        self.assertEqual(obj_2.shares.count(), 0)
        self.assertEqual(obj_3.shares.count(), 0)

        ShareClass = TestSharedObjectModel.get_share_class()
        shares = ShareClass.objects.create_many(objs=objs,
                                                for_user=user,
                                                created_user=user,
                                                status=Status.ACCEPTED)
        self.assertEqual(obj_1.shares.count(), 1)
        self.assertEqual(obj_2.shares.count(), 1)
        self.assertEqual(obj_3.shares.count(), 1)

    def test_create_many_prevent_duplicate_share(self):
        """Test the ``create_many`` method that ensure no duplicate shares are
        created for a single user.
        """
        user = create_user()
        obj_1 = TestSharedObjectModel.objects.create()
        obj_1.shares.create_for_user(for_user=user,
                                     created_user=user,
                                     status=Status.ACCEPTED)
        self.assertEqual(obj_1.shares.count(), 1)

        obj_2 = TestSharedObjectModel.objects.create()
        obj_3 = TestSharedObjectModel.objects.create()
        objs = [obj_1, obj_2, obj_3]

        ShareClass = TestSharedObjectModel.get_share_class()
        shares = ShareClass.objects.create_many(objs=objs,
                                                for_user=user,
                                                created_user=user,
                                                status=Status.ACCEPTED)
        self.assertEqual(obj_1.shares.count(), 1)
        self.assertEqual(obj_2.shares.count(), 1)
        self.assertEqual(obj_3.shares.count(), 1)
