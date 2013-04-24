# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
# from django_sharing.models import SharePending
from django.contrib.contenttypes import generic
from django_sharing.models import Share
# from django_sharing.models import Share

# class SimpleDocShareMixin(object):
#    """Sharing mixing for a document.
#
#    Fields:
#
#    * share_user_ids: the current list of user ids sharing this object.
#
#    """
#    share_user_ids = ListField(db_field='suids')
#
#
#    def add_share(self, for_user_id, additional_updates=None, auto_save=True):
#        """Adds a share to a document.
#
#        :param for_user_id: id of the user sharing this document.
#        :param auto_save: boolean indicating if the document should make a call
#            to mongo to add the share to the document. If false, just appends
#            the share to self.
#
#        """
#        self.add_shares(for_user_ids=[for_user_id],
#                        additional_updates=additional_updates,
#                        auto_save=auto_save)
#
#    def add_shares(self, for_user_ids, additional_updates=None, auto_save=True):
#        """Adds many user shares to the to the doc class.
#
#        :param additional_updates: additional updates to make on the selected
#            documents.
#
#        """
#        if auto_save:
#
#            updates = {'add_to_set__share_user_ids': for_user_ids}
#
#            if additional_updates:
#                updates.update(**additional_updates)
#
#            self.__class__.objects(id=self.id).update_one(**updates)
#            self.reload()
#        else:
#            for user_id in for_user_ids:
#                if user_id not in self.share_user_ids:
#                    self.share_user_ids.append(user_id)
#
#    def is_shared_by_user(self, for_user_id):
#        """Check to see if this document is shared by a specific user.
#
#        Returns a boolean True if this user is sharing this document.
#        Otherwise, False.
#
#        """
#        if not for_user_id:
#            return False
#
#        return for_user_id in self.share_user_ids
#
#    def remove_share(self, for_user_id, additional_updates=None,
#                     auto_save=True):
#        """Removes user sharing this doc.  Returns true if the user was removed.
#        Otherwise, returns False.
#
#        """
#        self.remove_shares(for_user_ids=[for_user_id],
#                           auto_save=auto_save,
#                           additional_updates=additional_updates)
#
#    def remove_shares(self, for_user_ids, additional_updates=None,
#                      auto_save=True):
#        """Removes users sharing this doc.  Returns true if the user was removed.
#        Otherwise, returns False.
#
#        """
#        if auto_save:
#            try:
#                updates = {'pull_all__share_user_ids': for_user_ids}
#                if additional_updates:
#                    updates.update(**additional_updates)
#
#                self.__class__.objects(id=self.id).update_one(**updates)
#                self.reload()
#            except self.__class__.DoesNotExist:
#                return self
#        else:
#            self.share_user_ids = [uid for uid in self.share_user_ids
#                                   if uid not in for_user_ids]


class ShareMixin(models.Model):
    """Document Sharing mixing that adds a shares list field which stores 
    additional metadata about a users share.
    
    :param share_embedded_document: this should be a sub class of BaseEmbeddedDocument
    :param shares: list of current sharing objects for specific users.
    
    """

#    meta = {'share_embedded_document': BaseShareEmbeddedDocument}
#    shares = ListField(EmbeddedDocumentField(meta['share_embedded_document']),
#                       db_field='sh')
#    shares = generic.GenericRelation(Share)

    class Meta:
        abstract = True

    def add_share(self, for_user_id, additional_updates=None, auto_save=True,
                  **share_kwargs):
        """Adds the user id to the list of sharing user ids and add a share 
        objects with associated metadata for the 'shares_class' embedded 
        Document.
        
        :param for_user_id: the id of the user the share is for.
        :param additional_updates: dictionary of additional updates to pass to
            the queryset update method. This is only applicable if 
            auto_save=True.
        :param auto_save: if True, will save the document after adding the share.
            If False, the .save() will have to be explicitly called after 
            calling this method.  This also allow for many shares to be added to
            a single bill before saving.
        :param share_kwargs: the kwargs for a specific user share that are 
            kwargs for the share_embedded_document.
        
        """
        share = self._meta['share_embedded_document'](for_user_id=for_user_id, **share_kwargs)

        if auto_save:
            if not additional_updates:
                additional_updates = {}

            additional_updates['add_to_set__shares'] = share
        else:
            self.shares.append(share)

        super(ShareMixin, self).add_share(for_user_id=for_user_id,
                                             additional_updates=additional_updates,
                                             auto_save=auto_save)

    def add_shares(self, for_user_ids, additional_updates=None, auto_save=True):
        """Adds many user shares to the to the doc class.
        
        :param additional_updates: additional updates to make on the selected
            documents.
            
        """
        if auto_save:

            updates = {'add_to_set__share_user_ids': for_user_ids}

            if additional_updates:
                updates.update(**additional_updates)

            self.__class__.objects(id=self.id).update_one(**updates)
            self.reload()
        else:
            for user_id in for_user_ids:
                if user_id not in self.share_user_ids:
                    self.share_user_ids.append(user_id)

    def is_shared_by_user(self, for_user_id):
        """Check to see if this document is shared by a specific user.
        
        Returns a boolean True if this user is sharing this document.  
        Otherwise, False.
        
        """
        if not for_user_id:
            return False

        return for_user_id in self.share_user_ids

    def remove_share(self, for_user_id, auto_save=True):
        """Remove share for a user id"""
        self.remove_shares(for_user_ids=[for_user_id],
                           auto_save=auto_save)

    def remove_shares(self, for_user_ids, auto_save=True):
        """Remove shares for a list of user ids.
        
        :param for_user_ids: a list of of user ids to remove the share for.
        
        """
        additional_updates = None

        shares = [share for share in self.shares
                  if share.for_user_id not in for_user_ids]

        if auto_save:
            # Can't do a pull_all operation here because you can't do a pull all
            # on nested dicts in mongoengine.  So just set the share objects.
            additional_updates = {'set__shares': shares}
        else:
            self.shares = shares

        super(ShareMixin, self).remove_shares(for_user_ids=for_user_ids,
                                                 additional_updates=additional_updates,
                                                 auto_save=auto_save)

    def get_share_for_user_id(self, for_user_id):
        """Get a share object for a specified user id.
        
        :param for_user_id: the id of the user to get the share for.
        :param return the share_embedded_document object for the specific user.
            If no share for this user id is found, return None

        """
        if not self.shares:
            return None

        for share in self.shares:
            if share.for_user_id == for_user_id:
                return share


class SharePendingMixin(models.Model):
    """Pending sharing mixin use to represent a document that wants to be 
    shared with a user.  The user can either be an existing site user or 
    potential future site user.
    
    Fields:
    
    * pending_shares_class: pending share class to use as the embedded document 
        field for pending shares.
    * pending_shares: list of pending share objects.
    
    """
#    meta = {'pending_share_embedded_document': BaseSharePendingEmbeddedDocument}
#    pending_shares = ListField(EmbeddedDocumentField(meta['pending_share_embedded_document']),
#                               db_field='ps')

#    pending_shares = models.ForeignKey(SharePending, null=True, blank=True)
    pending_shares = generic.GenericRelation(Share)

    class Meta:
        abstract = True

    def add_pending_share(self, auto_save=True, **kwargs):
        """Adds a pending share for the doc.
        
        :param pending_share: arguments for pending_shares.
        :param auto_save: makes a call to mongo to add the share to the document.
            If false, just appends the share to self.
        :param kwargs: keyword arguments for the pending_share_embedded_document 
            class.
        :return: the token for the new pending share.
        
        """
        utcnow = datetime.utcnow()
        kwargs['last_sent'] = utcnow
        kwargs['last_modified_dttm'] = utcnow
        pending_share = self._meta['pending_share_embedded_document'](**kwargs)

        if auto_save:
            self.__class__.objects(id=self.id).update_one(add_to_set__pending_shares=pending_share)
            self.reload()
        else:
            self.pending_shares.append(pending_share)

        return pending_share.token

    def update_pending_share(self, token, auto_save=True, **kwargs):
        """Updates an existing pending share for a doc.  You must include an
        email address or a for_user. They both can't be empty.
        
        :param token: the pending share token used to update the pending request.
        :param kwargs: any kwargs that the pending_share_embedded_document 
            accepts.
        :return: the pending share token.
        
        """
        def _get_db_key(field_name):
            """Gets the correct key for the class since it's not being 
            referenced correctly when the fields are given a db field name when 
            the pending_share_embedded_document is overridden."""
            return self._meta['pending_share_embedded_document']._db_field_map.get(field_name,
                                                                          field_name)

        utcnow = datetime.utcnow()
        kwargs['last_sent'] = utcnow
        kwargs['last_modified_dttm'] = utcnow

        if auto_save:
            updates = {}
            for field_name, value in kwargs.items():
                updates['set__pending_shares__S__{0}'.format(_get_db_key(field_name))] = value

            self.__class__.objects(id=self.id,
                                   pending_shares__token=token).update_one(**updates)
            self.reload()
            return token

        pending_share = self.get_pending_share_by_token(token)

        for key, value in kwargs.items():
            setattr(pending_share, key, value)

        return token


    def get_pending_share_by_user_id(self, user_id):
        """Gets a pending share object for this group by the user_id the share 
        is for.
        """
        if not self.pending_shares:
            return None

        for share in self.pending_shares:
            if share.for_user_id == user_id:
                return share

    def get_pending_share_by_token(self, token):
        """Gets a pending share object for this group by the sharing token.
        
        :param token: the token associated with the pending share.
        
        """

        if not self.pending_shares:
            return None

        for share in self.pending_shares:
            if share.token == token:
                return share

    def remove_pending_share_by_token(self, token, auto_save=True):
        """Removes a pending share by sharing token.
        
        :param token: the pending share token to remove from the pending requests.
        :param auto_save: makes a call to mongo to remove the shares to the 
            document by token. If false, just removes the share from self.
            
        """
        if auto_save:
            self.__class__.objects(id=self.id).update_one(pull__pending_shares__token=token)
            self.reload()
        else:
            self.pending_shares = [ps for ps in self.pending_shares
                                   if ps.token != token]
        return True

    def remove_pending_shares_by_tokens(self, tokens, auto_save=True):
        """Removes a pending share by sharing token.
        
        :param token: the pending share token to remove from the pending requests.
        :param auto_save: makes a call to mongo to remove the shares to the 
            document by token. If false, just removes the share from self.
            
        """
        if auto_save:
            self.__class__.objects(id=self.id).update_one(pull_all__pending_shares__token=tokens)
            self.reload()
        else:
            self.pending_shares = [ps for ps in self.pending_shares
                                   if ps.token not in tokens]
        return True

    def remove_pending_share_by_user_id(self, for_user_id, auto_save=True):
        """Removes a pending share for a user by the user id.  
        
        :param for_user_id: removes the pending share for a user by a user id.
        :param auto_save: makes a call to mongo to remove the shares to the 
            document by user_id. If false, just removes the share from self.
            
        """
        if auto_save:
            self.__class__.objects(id=self.id).update_one(pull__pending_shares__for_user_id=for_user_id)
            self.reload()
        else:
            self.pending_shares = [ps for ps in self.pending_shares
                                   if ps.for_user_id != for_user_id]
        return True

    def remove_pending_shares_by_user_ids(self, for_user_ids, auto_save=True):
        """Removes a pending share for a user by the user id.  
        
        :param for_user_id: removes the pending share for a user by a user id.
        :param auto_save: makes a call to mongo to remove the shares to the 
            document by user_id. If false, just removes the share from self.
            
        """
        if auto_save:
            self.__class__.objects(id=self.id).update_one(pull_all__pending_shares__for_user_id=for_user_ids)
            self.reload()
        else:
            self.pending_shares = [ps for ps in self.pending_shares
                                   if ps.for_user_id not in for_user_ids]
        return True
