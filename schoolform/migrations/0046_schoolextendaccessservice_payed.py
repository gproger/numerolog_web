# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-12-31 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0045_schoolextendaccessservice_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolextendaccessservice',
            name='payed',
            field=models.BooleanField(default=False),
        ),
    ]
