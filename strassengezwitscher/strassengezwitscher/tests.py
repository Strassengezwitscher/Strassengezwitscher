from django.core.urlresolvers import reverse
from django.test import TestCase


class StrassengezwitscherTests(TestCase):
    def test_serves_angular_tag(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<sg-app>', response.content)
        self.assertIn(b'</sg-app>', response.content)
