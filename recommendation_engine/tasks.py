from django.contrib.auth.models import User
from django_rq import job

from .recommender import Recommender
from .mailer import Mailer


@job
def send_recommendations(user: User):
    recommender = Recommender(user)
    photos = recommender.process()

    mailer = Mailer()
    mailer.send_recommendations(user.email, photos)
