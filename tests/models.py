# -*- coding: utf-8 -*-
from django.db import models
from django_sharing.models import AbstractShare
# from django_sharing.models import AbstractSharePending


class Car(models.Model):
    """A model that I will share."""
    # Because of reverse relations, this model will have the following two fields
    # shares

# class CarSharePending(AbstractSharePending):
#    """A vanilla test model for pending shares."""
#    desired_day = models.CharField(max_length=50)
#    car = models.ForeignKey(Car, related_name='pending_shares')


class CarShare(AbstractShare):
    """A vanilla test model for sharing for a car."""
    day = models.CharField(max_length=50)
    car = models.ForeignKey(Car, related_name='shares')
