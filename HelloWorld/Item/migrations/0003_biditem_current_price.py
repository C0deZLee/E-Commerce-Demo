# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0002_auto_20161107_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='biditem',
            name='current_price',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
    ]
