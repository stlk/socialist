from django.contrib.auth.models import User

from .models import UserAggregation

import numpy as np  # a conventional alias
import sklearn.feature_extraction.text as text
from sklearn.metrics.pairwise import euclidean_distances


class UserDistance():

    def __init__(self, user: User):
        self.username = user.username

    def generate_dtm(self, media_captions):
        vectorizer = text.CountVectorizer(input='content',
                                          strip_accents='ascii',
                                          stop_words='english')
        dtm = vectorizer.fit_transform(media_captions).toarray()
        self.dist = euclidean_distances(dtm)

    def find_distance(self, medium):
        return self.dist[self.usernames.index(medium['username']),
                         self.usernames.index(self.username)]

    def assign_user_distances(self, media):
        self.usernames = list(UserAggregation.objects.all().values_list('username', flat=True))
        media_captions = list(UserAggregation.objects.all().values_list('raw_text', flat=True))

        self.generate_dtm(media_captions)

        distance_threshold = np.max(self.dist) - np.mean(self.dist) * 2

        for medium in media:
            distance = self.find_distance(medium)
            medium['distance'] = distance
            medium['recommended'] = distance < distance_threshold
