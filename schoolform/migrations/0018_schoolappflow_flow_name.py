# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-12-19 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0017_auto_20191025_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappflow',
            name='flow_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
