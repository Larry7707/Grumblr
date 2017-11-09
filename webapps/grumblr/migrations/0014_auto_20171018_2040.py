# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0013_auto_20171017_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='last_changed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
