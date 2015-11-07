import os
import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialist.settings')

app = celery.Celery('socialist')
app.config_from_object('django.conf:settings')


from .instagram import Instagram
from .mailer import Mailer

from django.contrib.auth.models import User


@app.task
def send_recommendations(user: User):
    instagram = Instagram(user)
    photos = instagram.recommend()

    mailer = Mailer()
    mailer.send_recommendations(user.email, photos)
