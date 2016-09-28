from django.test import TestCase
from django.contrib.auth.models import User

from blogs.models import BlogEntry

from datetime import datetime


class BlogModelTests(TestCase):

    fixtures = ['users_views_testdata']

    def test_representations(self):
        title = 'EntryTitle'
        content = '<p> awesome html </p>'
        created_on = datetime.now
        created_by = User.objects.get(pk=1)
        status = BlogEntry.DRAFT
        blog_entry = BlogEntry(
            title=title,
            content=content,
            status=status,
            created_on=created_on,
            created_by=created_by,
            )
        representation = "<BlogEntry title='{}' created_by='{}' status='{}' >".format(title, created_by, status)

        self.assertEqual(str(blog_entry), representation)
        self.assertEqual(repr(blog_entry), representation)
