from __future__ import unicode_literals

from django.db import models

class MapObject(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
