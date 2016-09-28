from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event
from facebook.models import FacebookPage
from ckeditor.fields import RichTextField

from datetime import datetime

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class BlogEntry(models.Model):
    HIDDEN = 'HIDDEN'
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    BLOG_ENTRY_CHOICES = (
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
        (HIDDEN, 'hidden'),
    )

    title = models.CharField(max_length=100)
    content = RichTextField()
    status = models.CharField(
        max_length=15,
        choices=BLOG_ENTRY_CHOICES,
        default=DRAFT)

    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, unique=False)
    events = models.ManyToManyField(Event, blank=True, related_name="blog_entries")
    facebook_pages = models.ManyToManyField(FacebookPage, blank=True, related_name="blog_entries")

    def is_published(self):
        return self.status == self.PUBLISHED

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.pk})

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<BlogEntry title='{}' created_by='{}' status='{}' >".format(self.title, self.created_by, self.status)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')
