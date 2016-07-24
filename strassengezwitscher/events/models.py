from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from strassengezwitscher.models import MapObject


@python_2_unicode_compatible
class Event(MapObject):
    date = models.DateField()
    repetition_cycle = models.CharField(max_length=50, default='unbekannter Rhythmus')
    organizer = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    counter_event = models.BooleanField(default=False)
    coverage = models.BooleanField(default=False)
    participants = models.CharField(max_length=20, blank=True)

    def __repr__(self):
        name = self.name + ' ' if self.name else ''
        date = 'at %s' % self.date.strftime('%Y-%m-%d')
        organizer = ' by %s' % self.organizer if self.organizer else ''
        return '<Event ' + name + date + organizer + '>'

    def __str__(self):
        name = self.name + ' ' if self.name else ''
        date = 'at %s' % self.date.strftime('%Y-%m-%d')
        organizer = ' by %s' % self.organizer if self.organizer else ''
        return name + date + organizer

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
