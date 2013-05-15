# -*- coding: utf-8 -*-
import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from django_sharing.models import Share
from django_sharing.constants import Status

User = get_user_model()

def random_string():
    return uuid.uuid4().hex[:8]

def random_user():
    random_username = random_string()
    random_email = '{0}@{1}.com'.format(random_string(), random_string())
    return User.objects.create_user(random_username, random_email)

class ShareTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once per test case"""
        super(ShareTests, cls).setUpClass()
        cls.user = random_user()

    def setUp(self):
        """Run once per test."""
        self.shared_user = random_user()

    def test_add_for_user(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        self.assertEqual(share.shared_object, self.shared_user)

    def test_add_for_non_user(self):
        """Share a user object with a another user."""
        first_name = 'Jimmy'
        last_name = 'Buffet'
        email = 'hello@world.com'
        message = 'Share with me.'
        status = Status.PENDING
        share = Share.objects.create_for_non_user(created_by_user=self.user,
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
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_for_user(user=self.user)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_for_user_id(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_for_user_id(user_id=self.user.id)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_email(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_by_email(email=self.user.email)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_get_by_token(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        share_db = Share.objects.get_by_token(token=share.token)

        self.assertEqual(share, share_db)

    def test_get_by_shared_object(self):
        """Share a user object with a another user."""
        # self.assertEqual(self.car.shares, [])
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        shares = Share.objects.get_by_shared_object(obj=self.shared_user)

        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0], share)

    def test_accept_share(self):
        """Test for accepting share."""
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)
        self.assertEqual(share.status, Status.PENDING)

        first_name = 'Test first name'
        share.accept(first_name=first_name)
        self.assertEqual(share.status, Status.ACCEPTED)
        self.assertEqual(share.first_name, first_name)

    def test_decline_share(self):
        """Test for accepting share."""
        share = Share.objects.create_for_user(created_by_user=self.user,
                                              for_user=self.user,
                                              shared_object=self.shared_user)

        share.decline()
        self.assertEqual(share.status, Status.DECLINED)