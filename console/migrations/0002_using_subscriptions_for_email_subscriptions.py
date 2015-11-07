# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='instagram_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='last_media_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='object_type',
        ),
        migrations.AddField(
            model_name='subscription',
            name='cancelled',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 7, 16, 57, 40, 66599, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
