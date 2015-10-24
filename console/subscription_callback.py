from instagram import subscriptions
from .tasks import process_photo_update

def enqueue_photo_update(update):
    process_photo_update.delay(update)

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, enqueue_photo_update)
