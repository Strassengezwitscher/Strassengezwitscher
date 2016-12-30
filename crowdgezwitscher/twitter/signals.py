from django.db.models.signals import post_save
from django.dispatch import receiver

from twitter.models import TwitterAccount


@receiver(post_save, sender=TwitterAccount, dispatch_uid="fetch_initial_tweets")
def fetch_initial_tweets(sender, instance, **kwargs):
    instance.fetch_initial_tweets()
