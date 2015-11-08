import logging
from django.contrib.auth.models import User

from .tasks import send_recommendations

class Newsletter():

    def send(self, user: User):
        send_recommendations.delay(user)

    def send_to_all_subscribers(self):
        users = User.objects.filter(subscription__id__isnull=False, subscription__cancelled=None)
        for user in users:
            logging.info('Sending newsletter to %s', user.username)
            self.send(user)
        return users

    def send_to_one_subscriber(self, user_id: int):
        user = User.objects.filter(subscription__id__isnull=False, subscription__cancelled=None).get(id=user_id)
        logging.info('Sending newsletter to %s', user.username)
        self.send(user)
        return user
