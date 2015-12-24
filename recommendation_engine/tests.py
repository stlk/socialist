from django.test import TestCase
from unittest.mock import patch, Mock, PropertyMock
from instagram.client import InstagramAPI
from .related_photos import RelatedPhotos
from .user_distance_data import UserDistanceData
from .models import UserAggregation


class MockInstagramAPI(InstagramAPI):

    def __init__(self, access_token, client_secret):
        tag = Mock()
        type(tag).name = PropertyMock(return_value='tag')
        user = Mock()
        type(user).id = PropertyMock(return_value=1)
        type(user).username = PropertyMock(return_value='username')
        caption = Mock()
        type(caption).text = PropertyMock(return_value='caption')
        medium = Mock(id=1,
                      like_count=1,
                      link='',
                      get_standard_resolution_url=Mock(return_value=''),
                      user=user,
                      caption=caption)
        type(medium).tags = PropertyMock(return_value=[tag])

        self.medium = medium

    def user_liked_media(self, with_next_url=None):
        return [self.medium], None

    def tag_recent_media(self, tag_name, with_next_url=None):
        return [self.medium], None

    def user_recent_media(self, user_id=None, with_next_url=None):
        return [self.medium], None


@patch('django.contrib.auth.models.User')
@patch('recommendation_engine.instagram.InstagramAPI', new=MockInstagramAPI)
class RelatedPhotosTest(TestCase):

    def test_recommend_returns_correct_data(self, User):
        user = User()

        related_photos = RelatedPhotos(user)
        recommendations = related_photos.recommend()

        self.assertEqual(recommendations[0]['tags'][0], 'tag')


@patch('django.contrib.auth.models.User')
@patch('recommendation_engine.instagram.InstagramAPI', new=MockInstagramAPI)
class UserDistanceDataTest(TestCase):

    def test_recommend_returns_correct_data(self, User):
        user = User()

        user_distance_data = UserDistanceData(user)
        user_distance_data.get_user_aggregations([1])

        aggregation = UserAggregation.objects.get(user_id=1)
        self.assertEqual(aggregation.raw_text, 'caption')
