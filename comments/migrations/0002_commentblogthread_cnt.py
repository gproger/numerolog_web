# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-15 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentblogthread',
            name='cnt',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
