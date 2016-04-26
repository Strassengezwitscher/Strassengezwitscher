from __future__ import unicode_literals

from django.db import models
from mapobjects.models import MapObject

class Event(MapObject):
    date = models.DateField()
    repetition_cycle = models.CharField(max_length=50)
    organizer = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    link_to_event = models.URLField()
    counter_event = models.BooleanField()
    coverage = models.BooleanField()
