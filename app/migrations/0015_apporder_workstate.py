# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-10-08 09:44
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_appautogeneratoroptions_serv_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='apporder',
            name='workstate',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
