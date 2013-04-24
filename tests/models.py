# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.db import models
from django_sharing.models import Share


class CarShare(Share):
    """A vanilla test model for extending the sharing Model for a car."""
    day = models.CharField(max_length=50)
    car = models.ForeignKey('Car', related_name='shares')


class Car(models.Model):
    """A model that I will share."""
    # Because of reverse relations, this model will have the following two fields
    # shares
    shares = generic.GenericRelation(CarShare)
