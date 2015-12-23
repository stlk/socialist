from django.test import TestCase
from unittest.mock import patch, Mock, PropertyMock
from instagram.client import InstagramAPI
from .related_photos import RelatedPhotos


class MockInstagramAPI(InstagramAPI):

    def __init__(self, access_token, client_secret):
        tag = Mock()
        type(tag).name = PropertyMock(return_value='tag')
        user = Mock()
        type(user).username = PropertyMock(return_value='username')
        medium = Mock(id=1,
                      like_count=1,
                      link='',
                      get_standard_resolution_url=Mock(return_value=''),
                      user=user)
        type(medium).tags = PropertyMock(return_value=[tag])

        self.medium = medium

    def user_liked_media(self, with_next_url=None):
        return [self.medium], None

    def tag_recent_media(self, tag_name, with_next_url=None):
        return [self.medium], None


@patch('django.contrib.auth.models.User')
@patch('recommendation_engine.instagram.InstagramAPI', new=MockInstagramAPI)
class RelatedPhotosTest(TestCase):

    def test_recommend_returns_correct_data(self, User):
        user = User()

        related_photos = RelatedPhotos(user)
        recommendations = related_photos.recommend()

        self.assertEqual(recommendations[0]['tags'][0], 'tag')
