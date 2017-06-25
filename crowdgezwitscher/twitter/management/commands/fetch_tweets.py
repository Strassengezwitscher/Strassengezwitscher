from django.core.management.base import BaseCommand, CommandError

from twitter.models import TwitterAccount


class Command(BaseCommand):
    help = 'Fetches new tweets for all or specified twitter accounts.'

    def add_arguments(self, parser):
        parser.add_argument('-a, --account_id',
                            metavar='ACCOUNT_ID',
                            dest='account_ids',
                            nargs='+',
                            type=int,
                            help='Database ID(s) of a TwitterAccount instance')

    def handle(self, *args, **options):
        account_ids = options['account_ids']
        if account_ids:
            try:
                accounts = [TwitterAccount.objects.get(pk=id) for id in account_ids]
            except TwitterAccount.DoesNotExist:
                raise CommandError('"%s" includes non-existent TwitterAccount IDs' % account_ids)
        else:
            accounts = TwitterAccount.objects.all()

        for account in accounts:
            account.fetch_tweets()
