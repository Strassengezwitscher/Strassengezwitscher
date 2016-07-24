from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class MapObject(models.Model):
    name = models.CharField(max_length=100, default="unbenannt")
    active = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)

    def __repr__(self):
        return '<MapObject %s>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
