# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20161107_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]