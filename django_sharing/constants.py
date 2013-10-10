# -*- coding: utf-8 -*-


class Status():
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
