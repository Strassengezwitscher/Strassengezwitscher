from __future__ import unicode_literals

from django.db import models
from mapobjects.models import MapObject

class FacebookPage(MapObject):
    link_to_facebook = models.URLField()


class FacebookLikeStatistic(models.Model):
    date = models.DateField()
    like_count = models.PositiveIntegerField()
