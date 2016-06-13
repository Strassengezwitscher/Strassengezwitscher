from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mapobjects.models import MapObject
from events.models import Event


@python_2_unicode_compatible
class FacebookPage(MapObject):
    url = models.URLField()
    events = models.ManyToManyField(Event, blank=True)

    def __repr__(self):
        return '<FacebookPage %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('facebook:detail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class FacebookLikeStatistic(models.Model):
    date = models.DateField()
    like_count = models.PositiveIntegerField()
    page = models.ForeignKey(FacebookPage, null=True)

    def __repr__(self):
        return '<FacebookLikeStatistic at %s>' % self.date.strftime('%Y-%m-%d')

    def __str__(self):
        return '%d at %s' % (self.like_count, self.date.strftime('%Y-%m-%d'))
