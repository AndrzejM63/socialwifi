# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_list', '0002_auto_20170307_0839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='feed',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
