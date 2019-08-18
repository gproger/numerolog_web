# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-11 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappflow',
            name='state',
            field=models.IntegerField(choices=[(0, 'created'), (1, 'recruitment'), (2, 'register'), (3, 'started'), (4, 'finished')], default=0),
        ),
    ]