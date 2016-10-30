from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import BlogEntry
from datetime import datetime


class BlogModelTests(TestCase):

    fixtures = ['users_views_testdata']

    def test_representations(self):
        title = 'EntryTitle'
        content = '<p> awesome html </p>'
        created_on = datetime.now
        created_by = User.objects.get(pk=1)
        status = BlogEntry.DRAFT
        blogentry = BlogEntry(
            title=title,
            content=content,
            status=status,
            created_on=created_on,
            created_by=created_by,
        )
        representation = "< BlogEntry title='{}' created_by='{}' status='{}' >".format(title, created_by, status)

        self.assertEqual(str(blogentry), representation)
        self.assertEqual(repr(blogentry), representation)
