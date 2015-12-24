from django.db import models


class UserAggregation(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200)
    raw_text = models.TextField(blank=False)
    media_count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
