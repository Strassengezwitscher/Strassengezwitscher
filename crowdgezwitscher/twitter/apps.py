from __future__ import unicode_literals

from django.apps import AppConfig


class TwitterConfig(AppConfig):
    name = 'twitter'

    def ready(self):
        import twitter.signals  # noqa
