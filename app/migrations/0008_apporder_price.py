# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-09-19 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_appresultfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='apporder',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
