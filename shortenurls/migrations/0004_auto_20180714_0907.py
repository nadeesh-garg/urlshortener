# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-14 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortenurls', '0003_auto_20180713_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlshortener',
            name='url',
        ),
        migrations.AddField(
            model_name='urlshortener',
            name='longurl',
            field=models.CharField(default='f', max_length=300),
            preserve_default=False,
        ),
    ]
