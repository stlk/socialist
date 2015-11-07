from .instagram import Instagram
from .mailer import Mailer

from django.contrib.auth.models import User

class Recommender():

    def recommend(self, user: User):
        instagram = Instagram(user)
        photos = instagram.recommend()

        mailer = Mailer()
        mailer.send_recommendations(user.email, photos)
