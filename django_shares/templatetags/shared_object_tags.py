# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def get_share_for_user(shares, user):
    """Gets the share for a specific user.

    :param shares: iterable of share objects
    :param user: the user the share is for
    """
    if not shares:
        return None

    for share in shares:
        if share.for_user_id == user.id:
            return share

    return None
