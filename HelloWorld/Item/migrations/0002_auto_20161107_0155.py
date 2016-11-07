# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biditem',
            name='item',
        ),
        migrations.AddField(
            model_name='item',
            name='bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='Item.BidItem', unique=True),
        ),
    ]