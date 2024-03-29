from django.urls import reverse
from django.db import models

from base.models import MapObject
from events.models import Event


class FacebookPage(MapObject):
    events = models.ManyToManyField(Event, blank=True, related_name="facebook_pages")
    facebook_id = models.CharField(max_length=50)

    def __repr__(self):
        return '<FacebookPage %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('facebook:detail', kwargs={'pk': self.pk})

    def url(self):
        return 'https://www.facebook.com/%s' % self.facebook_id


class FacebookLikeStatistic(models.Model):
    date = models.DateField()
    like_count = models.PositiveIntegerField()
    page = models.ForeignKey(FacebookPage, models.CASCADE, null=True)

    def __repr__(self):
        return '<FacebookLikeStatistic on %s for %s>' % (self.date.strftime('%Y-%m-%d'), self.page)

    def __str__(self):
        return '%d on %s for %s' % (self.like_count, self.date.strftime('%Y-%m-%d'), self.page)
