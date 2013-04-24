# -*- coding: utf-8 -*-
from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from tests.models import Car

User = get_user_model()


# class MockShareEmbeddedDocument(BaseShareEmbeddedDocument):
#    """Mock embedded sharing object to properly test inheritance."""
#    some_attribute = StringField(db_field='sa')
#
#
# class MockDocSharesMixinModel(AbstractBaseDocument, DocShareMixin):
#    """Mock model used for testing the base shares model mixin."""
#    meta = {'share_embedded_document': MockShareEmbeddedDocument}
#
#
# class MockSimpleDocSharesMixinModel(AbstractBaseDocument, SimpleDocShareMixin):
#    """Mock model used for testing the base shares model mixin."""
#    pass
#
#
# class MockBasePendingSharesMixinModel(AbstractBaseDocument, BasePendingSharesMixin):
#    """Mock model used for testing the base pending shares model mixin."""
#    pass
#
#
# class MockSharePendingEmbeddedDocument(BaseSharePendingEmbeddedDocument):
#    """Mock share pending embedded document that has an extra field."""
#    my_extra_share_attr = StringField(db_field='mesa')
#
#
# class MockPendingSharesCustomShareMixin(AbstractBaseDocument, BasePendingSharesMixin):
#    """Mock model for pending shares using a different share embedded object."""
#    meta = {'pending_share_embedded_document': MockSharePendingEmbeddedDocument}


class ShareTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once per test case"""
        super(ShareTests, cls).setUpClass()
        cls.usr = User.objects.create_user('john', 'john@doe.com', 'test')

    def setUp(self):
        """Run once per test."""
#        self.car = Car.objects.create()

    def test_add_for_user(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        shared_user = User.objects.create_user('Bill', 'bill@bow.com', 'pass')
        self.assertIsNone(self.usr)
        pass

#    def test_add_share(self):
#        """Test for adding a share to a document."""
#        self.assertEqual([], self.doc.share_user_ids)
#        self.doc.add_share(for_user_id=self.usr.id)
#        self.assertEqual([self.usr.id], self.doc.share_user_ids)
#
#        doc = MockSimpleDocSharesMixinModel.get_by_id(id=self.doc.id)
#        self.assertEqual(self.doc.share_user_ids, doc.share_user_ids)

#    def test_add_shares(self):
#        """Test for adding a shares to a document."""
#        self.assertEqual([], self.doc.share_user_ids)
#        user_id_1 = 1234
#        user_id_2 = 'xyz123'
#        user_id_3 = 54321
#        user_ids = [user_id_1, user_id_2, user_id_3]
#        self.doc.add_shares(for_user_ids=user_ids)
#        self.assertTrue(user_id_1 in self.doc.share_user_ids)
#        self.assertTrue(user_id_2 in self.doc.share_user_ids)
#        self.assertTrue(user_id_3 in self.doc.share_user_ids)
#
#        doc = MockSimpleDocSharesMixinModel.get_by_id(id=self.doc.id)
#        self.assertEqual(len(doc.share_user_ids), 3)
#        self.assertTrue(user_id_1 in doc.share_user_ids)
#        self.assertTrue(user_id_2 in doc.share_user_ids)
#        self.assertTrue(user_id_3 in doc.share_user_ids)
#
#    def test_is_shared_by_user(self):
#        """Test for seeing if a user is sharing a document."""
#        self.doc.add_share(for_user_id=self.usr.id, auto_save=False)
#        self.assertTrue(self.doc.is_shared_by_user(self.usr.id))
#
#    def test_remove_share(self):
#        """Test for removing a share from a document."""
#        self.doc.add_share(for_user_id=self.usr.id)
#        self.assertTrue(self.usr.id in self.doc.share_user_ids)
#
#        self.doc.remove_share(for_user_id=self.usr.id)
#        self.assertTrue(self.usr.id not in self.doc.share_user_ids)
#
#    def test_remove_shares(self):
#        """Test for removing shares from a document."""
#        user_id_1 = 1234
#        user_id_2 = 'xyz123'
#        user_id_3 = 54321
#        user_ids = [user_id_1, user_id_2, user_id_3]
#        self.doc.add_shares(for_user_ids=user_ids)
#
#        self.doc.remove_shares(for_user_ids=[user_id_2, user_id_3])
#        self.assertEqual([user_id_1], self.doc.share_user_ids)
#
#
# class DocSharesMixinTests(MongoTestCase):
#
#    @classmethod
#    def setUpClass(cls):
#        """Run once per test case"""
#        super(DocSharesMixinTests, cls).setUpClass()
#        cls.usr = User.objects.create(id=random_alphanum_id())
#
#    def setUp(self):
#        """Run once per test."""
#        self.doc = MockDocSharesMixinModel.objects.create()
#
#    def test_add_share(self):
#        share_attr_value = 'hello world'
#        self.doc.add_share(for_user_id=self.usr.id,
#                           some_attribute=share_attr_value)
#        self.assertEqual(len(self.doc.shares), 1)
#        self.assertEqual(self.doc.shares[0].some_attribute, share_attr_value)
#        doc = MockDocSharesMixinModel.get_by_id(id=self.doc.id)
#        self.assertEqual(self.doc.shares, doc.shares)
#
#    def test_remove_share(self):
#        """Test to remove share for a user id"""
#        self.doc.add_share(for_user_id=self.usr.id, auto_save=False)
#        self.assertEqual(len(self.doc.shares), 1)
#        self.assertEqual(self.doc.share_user_ids[0], self.usr.id)
#
#        self.doc.remove_share(for_user_id=self.usr.id, auto_save=False)
#        self.assertEqual(len(self.doc.shares), 0)
#
#    def test_remove_shares_auto_save_false(self):
#        """Test to remove shares for a user ids"""
#        user_id_1 = '12345'
#        user_id_2 = '98765'
#        self.doc.add_share(for_user_id=user_id_1, auto_save=False)
#        self.doc.add_share(for_user_id=user_id_2, auto_save=False)
#        self.doc.add_share(for_user_id=self.usr.id, auto_save=False)
#
#        self.assertEqual(len(self.doc.shares), 3)
#        self.assertTrue(user_id_1 in self.doc.share_user_ids)
#        self.assertTrue(user_id_2 in self.doc.share_user_ids)
#        self.assertTrue(self.usr.id in self.doc.share_user_ids)
#
#        self.doc.remove_shares(for_user_ids=[user_id_1, user_id_2],
#                               auto_save=False)
#        self.assertEqual(len(self.doc.shares), 1)
#        self.assertEqual(self.doc.shares[0].for_user_id, self.usr.id)
#
#    def test_remove_shares_auto_save_true(self):
#        """Test to remove shares for a user ids"""
#        user_id_1 = '12345'
#        user_id_2 = '98765'
#        self.doc.add_share(for_user_id=user_id_1)
#        self.doc.add_share(for_user_id=user_id_2)
#        self.doc.add_share(for_user_id=self.usr.id)
#
#        self.assertEqual(len(self.doc.shares), 3)
#        self.assertTrue(user_id_1 in self.doc.share_user_ids)
#        self.assertTrue(user_id_2 in self.doc.share_user_ids)
#        self.assertTrue(self.usr.id in self.doc.share_user_ids)
#
#        self.doc.remove_shares(for_user_ids=[user_id_1, user_id_2])
#        self.assertEqual(len(self.doc.shares), 1)
#        self.assertEqual(self.doc.shares[0].for_user_id, self.usr.id)
#
#    def test_get_share_for_user_id(self):
#        """Test for getting a share for a specific user id."""
#        share_1 = MockShareEmbeddedDocument()
#        share_2 = MockShareEmbeddedDocument(for_user_id=self.usr.id)
#        share_3 = MockShareEmbeddedDocument()
#
#        self.doc.shares = [share_1, share_2, share_3]
#        share = self.doc.get_share_for_user_id(for_user_id=self.usr.id)
#        self.assertEqual(share_2, share)
#
#
# class BasePendingSharesMixinTests(MongoTestCase):
#
#    @classmethod
#    def setUpClass(cls):
#        """Run once per test case"""
#        super(BasePendingSharesMixinTests, cls).setUpClass()
#        cls.usr = User.objects.create(id=random_alphanum_id())
#        cls.pending_share_kwargs = {
#            'email': 'hello@example.com',
#            'first_name': 'Jane',
#            'last_name': 'Doe',
#            'created_id': '12345',
#            'message': 'Hello world!  Come share something.'
#        }
#
#    def setUp(self):
#        """Run once per test."""
#        self.doc = MockPendingSharesCustomShareMixin.objects.create()
#
#    def test_add_pending_share(self):
#        """Test for adding a pending share to a document."""
#        self.doc.add_pending_share(for_user_id=self.usr.id,
#                                   **self.pending_share_kwargs)
#        self.assertEqual(len(self.doc.pending_shares), 1)
#        self.assertEqual(self.doc.pending_shares[0].for_user_id, self.usr.id)
#        self.assertEqual(self.doc.pending_shares[0].email,
#                         self.pending_share_kwargs['email'])
#        self.assertEqual(self.doc.pending_shares[0].first_name,
#                         self.pending_share_kwargs['first_name'])
#        self.assertEqual(self.doc.pending_shares[0].last_name,
#                         self.pending_share_kwargs['last_name'])
#        self.assertEqual(self.doc.pending_shares[0].created_id,
#                         self.pending_share_kwargs['created_id'])
#        self.assertEqual(self.doc.pending_shares[0].message,
#                         self.pending_share_kwargs['message'])
#        self.assertEqual(len(self.doc.pending_shares[0].token), 15)
#
#    def test_update_pending_share(self):
#        """Test for updating an existing pending share."""
#        token = self.doc.add_pending_share(for_user_id=self.usr.id,
#                                           **self.pending_share_kwargs)
#
#        email = 'email@example.com'
#        first_name = 'Tim'
#        last_name = 'Buck'
#        message = 'Some changed message text.'
#        my_extra_share_attr = 'Works'
#        # Need to replace the microseconds here because mongo doesn't store to
#        # the same precision that utcnow() function provides.
#        utc_before = datetime.utcnow().replace(microsecond=0)
#
#        self.doc.update_pending_share(token=token,
#                                      email=email,
#                                      first_name=first_name,
#                                      last_name=last_name,
#                                      message=message,
#                                      my_extra_share_attr=my_extra_share_attr)
#
#        pending_share = self.doc.get_pending_share_by_token(token=token)
#        self.assertEqual(pending_share.email, email)
#        self.assertEqual(pending_share.first_name, first_name)
#        self.assertEqual(pending_share.last_name, last_name)
#        self.assertEqual(pending_share.message, message)
#        self.assertEqual(pending_share.my_extra_share_attr, my_extra_share_attr)
#
#        utc_after = datetime.utcnow()
#        self.assertTrue(utc_before < pending_share.last_sent < utc_after)
#        self.assertTrue(utc_before < pending_share.last_modified_dttm < utc_after)
#
#        doc = self.doc.__class__.get_by_id(id=self.doc.id)
#        pending_share_db = doc.get_pending_share_by_token(token=token)
#
#        self.assertEqual(pending_share, pending_share_db)
#
#    def test_get_pending_share_by_user_id(self):
#        """Test for getting a pending share by user id."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        self.doc.add_pending_share(for_user_id=user_id_1,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        self.doc.add_pending_share(for_user_id=user_id_2,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        pending_share = self.doc.get_pending_share_by_user_id(user_id=user_id_2)
#        self.assertEqual(pending_share.for_user_id, user_id_2)
#
#
#    def test_get_pending_share_by_token(self):
#        """Test for getting a pending share by token."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        token_1 = self.doc.add_pending_share(for_user_id=user_id_1,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        token_2 = self.doc.add_pending_share(for_user_id=user_id_2,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        pending_share_1 = self.doc.get_pending_share_by_token(token=token_1)
#        self.assertEqual(pending_share_1.for_user_id, user_id_1)
#
#        pending_share_2 = self.doc.get_pending_share_by_token(token=token_2)
#        self.assertEqual(pending_share_2.for_user_id, user_id_2)
#
#    def test_remove_pending_share_by_token(self):
#        """Test for removing a pending share by token."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        token_1 = self.doc.add_pending_share(for_user_id=user_id_1,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        token_2 = self.doc.add_pending_share(for_user_id=user_id_2,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        self.assertEqual(len(self.doc.pending_shares), 2)
#        self.doc.remove_pending_share_by_token(token=token_1,
#                                               auto_save=False)
#        self.assertEqual(len(self.doc.pending_shares), 1)
#        self.assertEqual(self.doc.pending_shares[0].for_user_id, user_id_2)
#
#
#    def test_remove_pending_share_by_tokens(self):
#        """Test for removing a pending shares by tokens."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        token_1 = self.doc.add_pending_share(for_user_id=user_id_1,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        token_2 = self.doc.add_pending_share(for_user_id=user_id_2,
#                                             auto_save=False,
#                                             **self.pending_share_kwargs)
#        self.assertEqual(len(self.doc.pending_shares), 2)
#        self.doc.remove_pending_shares_by_tokens(tokens=[token_1, token_2],
#                                               auto_save=False)
#        self.assertEqual(len(self.doc.pending_shares), 0)
#
#    def test_remove_pending_share_by_user_id(self):
#        """Test for removing a pending share by user id."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        self.doc.add_pending_share(for_user_id=user_id_1,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        self.doc.add_pending_share(for_user_id=user_id_2,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        self.assertEqual(len(self.doc.pending_shares), 2)
#        self.doc.remove_pending_share_by_user_id(for_user_id=user_id_1,
#                                                 auto_save=False)
#        self.assertEqual(len(self.doc.pending_shares), 1)
#        self.assertEqual(self.doc.pending_shares[0].for_user_id, user_id_2)
#
#    def test_remove_pending_share_by_user_ids(self):
#        """Test for removing a pending share by user ids."""
#        user_id_1 = '12345'
#        user_id_2 = '54321'
#        self.doc.add_pending_share(for_user_id=user_id_1,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        self.doc.add_pending_share(for_user_id=user_id_2,
#                                   auto_save=False,
#                                   **self.pending_share_kwargs)
#        self.assertEqual(len(self.doc.pending_shares), 2)
#        self.doc.remove_pending_shares_by_user_ids(for_user_ids=[user_id_1, user_id_2],
#                                                   auto_save=False)
#        self.assertEqual(len(self.doc.pending_shares), 0)
