from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from unittest.mock import patch

from .models import Subscription

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_returns_active_subscription(self):
        user = User.objects.create()
        subscription = Subscription.objects.create(user=user, instagram_id=1)
        self.assertEqual(user.subscription, subscription)


class NotificationViewTest(TestCase):

    def test_notification_handshake(self):
        response = self.client.get(reverse('console:notification') + '?hub.challenge=xxx')
        self.assertEqual(response.content.decode(), 'xxx')


class SubscribeViewTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(
            'user1',
            'user1@example.com',
            'pswd',
        )
        self.client.login(username="user1", password="pswd")

    def tearDown(self):
        self.client.logout()

    @patch('console.models.Subscription')
    def test_returns_OK_when_user_found(
        self, mock_subscription
    ):
        mock_subscription.subscribe_for_photos.return_value = {'id': 1, 'object': 'tag', 'object_id': 'xxx'}
        response = self.client.post(reverse('console:subscribe'), {'tag': 'xxx'})
        self.assertRedirects(response, reverse('console:stream'))
