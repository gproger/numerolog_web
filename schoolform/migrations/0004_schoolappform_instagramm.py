# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-13 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0003_auto_20190811_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappform',
            name='instagramm',
            field=models.CharField(default='test', max_length=80),
            preserve_default=False,
        ),
    ]