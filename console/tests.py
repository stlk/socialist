from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from unittest.mock import patch

from .models import Subscription

User = get_user_model()

class SubscriptionModelTest(TestCase):

    def test_user_returns_active_subscription(self):
        user = User.objects.create()
        subscription = user.subscription_set.create()
        self.assertEqual(user.subscription_set.get(), subscription)

    def test_unsubscribe_cancels_active_subscription(self):
        user = User.objects.create()
        subscription = user.subscription_set.create()
        Subscription.unsubscribe(user)
        subscription = user.subscription_set.get()
        self.assertIsNotNone(subscription.cancelled)

class SubscribeViewTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(
            'user1',
            '',
            'pswd',
        )
        self.client.login(username="user1", password="pswd")

    def tearDown(self):
        self.client.logout()

    def test_display_subscription_form_when_user_is_not_subscribed(self):
        response = self.client.get(reverse('console:subscribe'))
        self.assertTemplateUsed(response, 'subscribe.html')

    def test_redirect_to_subscribed_page_when_user_is_alredy_subscribed(self):
        user = User.objects.get(username='user1')
        subscription = Subscription.objects.create(user=user)
        response = self.client.get(reverse('console:subscribe'))

        self.assertRedirects(response, reverse('console:subscribed'))

    def test_save_users_email(self):
        response = self.client.post(reverse('console:subscribe'), {'email': 'email@example.com'})
        user = User.objects.get(username='user1')
        self.assertEqual(user.email, 'email@example.com')
