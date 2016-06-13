from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mapobjects.models import MapObject


@python_2_unicode_compatible
class Event(MapObject):
    date = models.DateField()
    repetition_cycle = models.CharField(max_length=50, default='unbekannter Rhythmus')
    organizer = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    url = models.URLField(blank=True, null=True)
    counter_event = models.BooleanField(default=False)
    coverage = models.BooleanField()

    def __repr__(self):
        return '<Event %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
