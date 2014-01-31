from __future__ import unicode_literals


def sort_shares_by_status(shares):
    """Sorts shares by status and returns a dict key'd by status type.

    :returns: tuple with the first part being the dictionary of shares
        keyed by their status, the second part being the auth users share.

    Example:

    (
        {'ACCEPTED': [...],
         'PENDING': [...]}
    )
    """
    share_by_status = {}

    for share in shares:

        if share.status in share_by_status:
            share_by_status[share.status].append(share)
        else:
            share_by_status[share.status] = [share]

    return share_by_status


def get_share_for_user(shares, user):
    """Gets the share object for a specific user.

    :param shares: iterable of shares
    :param user: user to get share for
    :return: the share object for the specified user or return None if not
        found.
    """
    for share in shares:
        if share.for_user_id == user.id:
            return share

    return None
