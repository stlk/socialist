from django.contrib.auth.models import User

from .related_photos import RelatedPhotos
from .user_distance_data import UserDistanceData
from .user_distance import UserDistance

RELATED_MEDIA_COUNT = 20
TOTAL_MEDIA_COUNT = 5


class Recommender():

    def __init__(self, user: User):
        self.related_photos = RelatedPhotos(user)
        self.user_distance_data = UserDistanceData(user)
        self.user_distance = UserDistance(user)

    def strip_unused_fields(self, collection):
        return list(map(lambda m:
                    {
                        'username': m['username'],
                        'caption': m['caption'],
                        'likes': m['likes'],
                        'link': m['link'],
                        'url': m['url'],
                        'tags': m['tags']
                    }, collection))

    def filter_recommended_photos(self, collection):
        collection = filter(lambda m: m['recommended'], collection)
        return self.strip_unused_fields(collection)[:TOTAL_MEDIA_COUNT]

    def process(self):
        recommended_photos = self.related_photos.recommend()[:RELATED_MEDIA_COUNT]

        recommended_user_ids = map(lambda m: m['user_id'], recommended_photos)

        self.user_distance_data.get_user_aggregations(recommended_user_ids)
        self.user_distance.assign_user_distances(recommended_photos)

        recommended_photos = self.filter_recommended_photos(recommended_photos)

        if len(recommended_photos) < TOTAL_MEDIA_COUNT:
            raise RuntimeError('Not enough photos')

        return recommended_photos
