# -*- coding: utf-8 -*-


class Status(object):
    """Sharing status.

    ACCEPTED: An accepted and active share
    DECLINED: declined share
    PENDING: pending share waiting on user's response
    INACTIVE: once an accepted share, now is no longer sharing
    """
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    PENDING = 'PENDING'
    INACTIVE = 'INACTIVE'
    CHOICES = ((ACCEPTED, 'Accepted'),
               (DECLINED, 'Declined'),
               (PENDING, 'Pending'),
               (INACTIVE, 'Inactive'))

    @classmethod
    def get_keys(cls):
        """Gets a tuple of all the status keys.

        (ACCEPTED, DECLINED, PENDING, INACTIVE)
        """
        return (choice[0] for choice in cls.CHOICES)
