# -*- coding: utf-8 -*-


class SharedObjectModelMixin(object):
    """Mixing for a shared object.  This model assumes you're calling the share
    field "shares".
    """

    def get_share_for_user(self, user):
        """Gets a share object for by the user the share is for."""
        return self.shares.get_or_none(for_user_id=user.id)

    def accept_pending_share(self, user, token):
        """
        Accepts a share for a user.
        
        :param user: user to accept the share for.
        :param token: token of the shared object
        """
        share = self.shares.get_by_token(token=token)

        # Need to verify this share is for the user passed in. Also, make sure
        # a share exists for the token passed in.
        if not share or share.for_user != user:
            return False

        return share.accept()

    def decline_pending_share(self, user, token):
        """
        Declines a share for a user.
        
        :param user: user to decline the share for.
        :param token: token of the shared object
        """
        share = self.shares.get_by_token(token=token)

        # Need to verify this share is for the user passed in. Also, make sure
        # a share exists for the token passed in.
        if not share or share.for_user != user:
            return False

        return share.decline()
