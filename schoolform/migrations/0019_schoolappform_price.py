# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-12-19 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0018_schoolappflow_flow_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappform',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]