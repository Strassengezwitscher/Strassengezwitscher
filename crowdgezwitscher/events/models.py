from __future__ import unicode_literals

import os
import random
import string

from PIL import Image

from django.conf import settings
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
    MAX_WIDTH = 256
    MAX_HEIGHT = 256

    def _get_path(self, filename):
        def random_string(length=5):
            symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
            return ''.join([random.choice(symbols) for _ in range(length)])

        filename_base, filename_ext = os.path.splitext(filename)
        return '{}/{}_{}_{}{}'.format('event_attachments',
                                      timezone_now().strftime("%Y/%m/%Y%m%d-%H%M"),
                                      filename_base.replace(' ', ''),
                                      random_string(),
                                      filename_ext.lower())

    def _get_path_and_set_filename(self, filename):
        """Takes the filename and returns where to store that file.

        Also saves the original file name in the `name` attribute.
        This method is called during creating of an Attachment instance, do not call it manually.
        """
        self.name = filename = os.path.basename(filename)
        return self._get_path(filename)

    attachment = models.FileField(upload_to=_get_path_and_set_filename)
    thumbnail = models.ImageField(blank=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='attachments')

    def __init__(self, *args, **kwargs):
        super(Attachment, self).__init__(*args, **kwargs)
        self.old_attachment = self.attachment

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Attachment %s for %s>" % (self.name, self.event)

    def save(self, *args, **kwargs):
        # Delete file and thumbnail from filesystem when attachment field is changed.
        if self.pk and self.attachment != self.old_attachment:
            # for building the thumbnail, we need the attachment attribute. that's why we must not use self instead
            # of instance. As we use save=False, the instance is not saved, just the files are removed from the
            # filesystem
            instance = Attachment.objects.get(pk=self.pk)
            instance.attachment.delete(save=False)
            instance.thumbnail.delete(save=False)

        # build thumbnail when creating Attachment instance or when changing attachment field
        if not self.pk or self.attachment != self.old_attachment:
            # delete any existing thumbnail. ok when no thumbnail exists. save() will be called later.
            self.thumbnail.delete(save=False)
            size = (self.MAX_WIDTH, self.MAX_HEIGHT)  # maximal width and height. aspect ratio is not changed.
            try:
                image = Image.open(self.attachment)
                image.thumbnail(size)

                # build a file path. remove original file extension and add ".thumbnail.jpg" instead.
                # ".jpg" leads to Pillow building a JPEG image
                file_path = os.path.splitext(self._get_path(self.attachment.name))[0] + ".thumbnail.jpg"

                absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
                image.save(absolute_file_path)

                self.thumbnail = file_path
            except Exception as e:  # noqa
                # lots of stuff can happen when trying to create thumbnails from broken images or files that are not
                # images at all.
                print("Error when creating thumbnail:", e)

        super(Attachment, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding `Attachment` instance is deleted."""
    instance.attachment.delete(save=False)
    instance.thumbnail.delete(save=False)
