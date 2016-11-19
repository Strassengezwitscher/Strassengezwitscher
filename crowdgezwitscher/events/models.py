from __future__ import unicode_literals

import os
import random
import string

from django.urls import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now as timezone_now

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
    twitter_account_names = models.CharField(max_length=150, blank=True)
    twitter_hashtags = models.CharField(max_length=150, blank=True)
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


@python_2_unicode_compatible
class Attachment(models.Model):

    def get_path_and_set_filename(self, filename):
        """Takes the filename and returns where to store that file.

        Also saves the original file name in the `name` attribute.
        This method is called during creating of an Attachment instance, do not call it manually.
        """

        def random_string(length=5):
            symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
            return ''.join([random.choice(symbols) for _ in range(length)])

        self.name = filename = os.path.basename(filename)
        filename_base, filename_ext = os.path.splitext(filename)
        return '{}/{}_{}_{}{}'.format('event_attachments',
                                      timezone_now().strftime("%Y/%m/%Y%m%d-%H%M"),
                                      filename_base.replace(' ', ''),
                                      random_string(),
                                      filename_ext.lower())

    attachment = models.FileField(upload_to=get_path_and_set_filename)
    name = models.CharField(max_length=50, blank=True)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='attachments')

    def __init__(self, *args, **kwargs):
        super(Attachment, self).__init__(*args, **kwargs)
        self.old_attachment = self.attachment

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Attachment %s for %s>" % (self.name, self.event)


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(**kwargs):
    """Deletes file from filesystem when corresponding `Attachment` instance is deleted."""
    kwargs['instance'].attachment.delete(save=False)


@receiver(models.signals.pre_save, sender=Attachment)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding `Attachment` instance's attachment field is changed."""
    if not instance.pk:  # file is created instead of changed
        return

    if instance.attachment != instance.old_attachment:
        try:
            Attachment.objects.get(pk=instance.pk).attachment.delete(save=False)
        except Attachment.DoesNotExist:
            return
