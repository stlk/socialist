import logging

from django.contrib.auth.models import User

from .related_photos import RelatedPhotos
from .user_distance_data import UserDistanceData


class Recommender():

    def process(self, user: User):
        related_photos = RelatedPhotos(user)
        user_distance_data = UserDistanceData(user)

        recommended_photos = related_photos.recommend()
        recommended_users = list(map(lambda m: m['user_id'], recommended_photos))
        user_distance_data.get_user_aggregations(recommended_users)
