# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-02-24 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsgate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneauthsms',
            name='t_id',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='phoneauthsms',
            name='type',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]