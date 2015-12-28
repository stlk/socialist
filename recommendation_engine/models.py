from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserAggregation(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200)
    raw_text = models.TextField(blank=False)
    media_count = models.IntegerField()
    tags = ArrayField(models.CharField(max_length=4000))
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
