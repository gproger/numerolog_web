# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-31 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apporder',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
