from django.conf import settings
from instagram import subscriptions
from instagram.client import InstagramAPI
import pusher

from .models import Subscription

p = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  ssl=True,
  port=443
)

def process_photo_update(update):
    """
    {'data': {}, 'subscription_id': 20423771, 'object': 'tag', 'changed_aspect': 'media', 'time': 1445180753, 'object_id': 'cat'}
    """
    print(update)

    subscription = Subscription.objects.get(instagram_id=update['subscription_id'])

    api = InstagramAPI(
        client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
        client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
    tag_recent_media, next = api.tag_recent_media(tag_name=update['object_id'], count=1, max_tag_id=subscription.last_media_id)

    if len(tag_recent_media) == 0:
        return
    media = tag_recent_media[0]
    if subscription.last_media_id == media.id:
        return

    photo = media.get_standard_resolution_url()
    subscription.last_media_id = media.id
    subscription.save()

    p.trigger('photos-{0}'.format(subscription.user.id), 'new', {'photo': photo})


reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_photo_update)
