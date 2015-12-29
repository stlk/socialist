from django.core.management.base import BaseCommand
from recommendation_engine.newsletter import Newsletter


class Command(BaseCommand):
    help = 'Sends newsletter to all subscribed users'

    def add_arguments(self, parser):
        parser.add_argument('user',
                            nargs='?',
                            type=int,
                            default=None,
                            help='Send newsletter to a single user')

    def handle(self, *args, **options):
        if options['user']:
            user = Newsletter().send_to_one_subscriber(options['user'])
            self.stdout.write('Successfully started generating newsletter for: %s' % user.username)
        else:
            users = Newsletter().send_to_all_subscribers()
            self.stdout.write('Successfully started generating newsletter for %d users' % len(users))
