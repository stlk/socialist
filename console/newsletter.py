import logging
from django.contrib.auth.models import User

from .tasks import send_recommendations

class Newsletter():

    def send(self, user: User):
        send_recommendations.delay(user)

    def send_to_all_subscribers(self):
        for user in User.objects.filter(subscription__cancelled=None):
            logging.info('Sending newsletter to %s', user.username)
            self.send(user)
