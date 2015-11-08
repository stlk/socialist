from django.contrib.auth.models import User
from django_rq import job

from .instagram import Instagram
from .mailer import Mailer


@job
def send_recommendations(user: User):
    instagram = Instagram(user)
    photos = instagram.recommend()

    mailer = Mailer()
    mailer.send_recommendations(user.email, photos)
