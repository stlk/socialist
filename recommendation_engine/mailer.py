import logging
from django.conf import settings
import sendwithus


class Mailer():

    def __init__(self):
        self.api = sendwithus.api(api_key=settings.SENDWITHUS_KEY)

    def send_recommendations(self, email, photos):
        r = self.api.send(
            email_id=settings.SENDWITHUS_TEMPLATE,
            recipient={'address': email},
            sender={'name': 'socialist.', 'address': 'socialist@post.rousek.name'},
            email_data={'photos': photos})
        if r.status_code == 200:
            logging.info('Sent email: {0}'.format(email))
        else:
            logging.warning('Mail didn\'t went through. {0}'.format(r.content))
