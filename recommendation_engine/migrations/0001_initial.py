# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAggregation',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('raw_text', models.TextField()),
                ('media_count', models.IntegerField()),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=4000))),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
