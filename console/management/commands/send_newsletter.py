from django.core.management.base import BaseCommand, CommandError
from console.newsletter import Newsletter

class Command(BaseCommand):
    help = 'Sends newsletter to all subscribed users'

    def handle(self, *args, **options):
        Newsletter().send_to_all_subscribers()
        self.stdout.write('Successfully started generating newsletter')
