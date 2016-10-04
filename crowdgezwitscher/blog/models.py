from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class BlogEntry(models.Model):
    HIDDEN = 'HIDDEN'
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    BLOGENTRY_CHOICES = (
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
        (HIDDEN, 'hidden'),
    )

    title = models.CharField(max_length=100)
    content = RichTextField()
    status = models.CharField(
        max_length=15,
        choices=BLOGENTRY_CHOICES,
        default=DRAFT)

    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, unique=False)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "< BlogEntry title='{}' created_by='{}' status='{}' >".format(self.title, self.created_by, self.status)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')
