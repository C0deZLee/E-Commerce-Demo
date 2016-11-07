# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 04:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Item', '0008_auto_20161107_0433'),
        ('Info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='Item.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='address',
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='owner',
        ),
        migrations.DeleteModel(
            name='CreditCard',
        ),
    ]
