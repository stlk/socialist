import logging

from django.conf import settings
from instagram.client import InstagramAPI

from django.contrib.auth.models import User


class Instagram():

    def __init__(self, user: User):
        self.api = InstagramAPI(
            access_token=user.social_auth.get().extra_data['access_token'],
            client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)

    def log_ratelimit(self):
        logging.info("Remaining API Calls: %s/%s",
                     self.api.x_ratelimit_remaining,
                     self.api.x_ratelimit)
