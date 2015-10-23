from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from instagram.client import InstagramAPI

from django.contrib.auth.models import User



class Subscription(models.Model):
    instagram_id = models.IntegerField()
    last_media_id = models.CharField(max_length = 50)
    object_type = models.CharField(max_length = 50)
    object_id = models.CharField(max_length = 100)
    user = models.ForeignKey(User)

    def subscribe(self, tag):
        """
        {'data': {'id': '20423789', 'aspect': 'media', 'type': 'subscription', 'object': 'tag', 'callback_url': '...', 'object_id': 'joseftaguje'}, 'meta': {'code': 200}}
        """
        api = InstagramAPI(
            client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
            client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
        callback_url = reverse('console:notification')
        subscription = api.create_subscription(object='tag', object_id=tag, aspect='media', callback_url=settings.HOSTNAME + callback_url)['data']
        self.instagram_id = subscription['id']
        self.object_type = subscription['object']
        self.object_id = subscription['object_id']
        self.save()
