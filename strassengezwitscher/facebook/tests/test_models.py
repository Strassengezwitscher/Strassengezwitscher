# pylint: disable=invalid-name,too-many-public-methods
from datetime import date

from django.test import TestCase

from facebook.models import FacebookPage, FacebookLikeStatistic


class FacebookPageModelTests(TestCase):
    def test_representation(self):
        page = FacebookPage(name='Test')
        self.assertEqual(repr(page), '<FacebookPage Test>')

    def test_string_representation(self):
        page = FacebookPage(name='Test')
        self.assertEqual(str(page), 'Test')


class FacebookLikeStatisticModelTests(TestCase):
    def test_representation(self):
        statistic = FacebookLikeStatistic(date=date(2012, 12, 21), like_count=42)
        self.assertEqual(repr(statistic), '<FacebookLikeStatistic at 2012-12-21>')

    def test_string_representation(self):
        statistic = FacebookLikeStatistic(date=date(2012, 12, 21), like_count=42)
        self.assertEqual(str(statistic), '42 at 2012-12-21')
