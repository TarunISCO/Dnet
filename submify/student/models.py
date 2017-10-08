# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from allauth.socialaccount.models import SocialAccount


# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(SocialAccount)
    email = models.EmailField()
    batch = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id) + " -> " + self.email

    def get_batch_id(self):
        batch_id = str(self.email)[0:4]
        return batch_id
