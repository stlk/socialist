import os
import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialist.settings')

app = celery.Celery('socialist')
app.config_from_object('django.conf:settings')


from .recommender import Recommender


@app.task
def send_recommendations(user):
    recommender = Recommender()
    recommender.recommend(user)
