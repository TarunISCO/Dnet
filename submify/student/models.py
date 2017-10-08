# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    image_url = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)

    def __str__(self):
        return self.username + " -> " + self.email

    def get_batch_id(self):
        batch_id = str(self.email)[0:4]
        return batch_id