from django.conf import settings
from instagram import subscriptions
from instagram.client import InstagramAPI
import pusher

p = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  ssl=True,
  port=443
)

def process_photo_update(update):
    print(update)

    api = InstagramAPI(
        client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
        client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
    tag_search, next_tag = api.tag_search(q=update['object_id'])
    tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name, count=1, max_tag_id=settings.LAST_PHOTO)
    if len(tag_recent_media) == 0:
        return
    media = tag_recent_media[0]
    print(media)
    if settings.LAST_PHOTO == media.id:
        return

    photo = media.get_standard_resolution_url()
    settings.LAST_PHOTO = media.id

    p.trigger('photos', 'new', {'photo': photo})


reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_photo_update)
