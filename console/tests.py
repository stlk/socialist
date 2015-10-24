from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_returns_active_subscription(self):
        user = User.objects.create()
        subscription = Subscription.objects.create(user=user, instagram_id=1)
        self.assertEqual(user.subscription, subscription)
