from __future__ import unicode_literals

from django.db import models
from mapobjects.models import MapObject
from events.models import Event


class FacebookPage(MapObject):
    link_to_facebook = models.URLField()
    events = models.ManyToManyField(Event)


class FacebookLikeStatistic(models.Model):
    date = models.DateField()
    like_count = models.PositiveIntegerField()
