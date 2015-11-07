from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    cancelled = models.DateTimeField(null = True)

    @classmethod
    def is_user_subscribed(cls, user: User) -> bool:
        return user.subscription_set.filter(cancelled=None).exists()

    @classmethod
    def subscribe(cls, user: User, email: str):
        user.email = email
        user.save()
        user.subscription_set.create()

    @classmethod
    def unsubscribe(cls, user: User):
        subscription = user.subscription_set.get(cancelled=None)
        subscription.cancelled = timezone.now()
        subscription.save()
