from __future__ import unicode_literals

from django.urls import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from crowdgezwitscher.models import MapObject


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
    coverage_start = models.DateField(blank=True, null=True)
    coverage_end = models.DateField(blank=True, null=True)

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

    def _is_ready_for_twitter(self):
        """Checks that all fields required for getting tweets have some value."""
        return all([self.twitter_account_names, self.coverage_start, self.coverage_end])

    def build_twitter_search_query(self):
        """Returns search query for Twitter from hashtags and account names."""
        if not self._is_ready_for_twitter():
            return
        accounts = [account.strip() for account in self.twitter_account_names.split(',')]
        accounts = [account[1:] if account[0] == '@' else account for account in accounts]  # remove leading '@'
        query = ' OR '.join(['from:%s' % acc for acc in accounts])
        if self.twitter_hashtags:
            hashtags = [hashtag.strip() for hashtag in self.twitter_hashtags.split(',')]
            hashtags = [hashtag if hashtag[0] == '#' else '#' + hashtag for hashtag in hashtags]  # require leading '#'
            query += ' %s' % ' OR '.join(hashtags)
        return query
