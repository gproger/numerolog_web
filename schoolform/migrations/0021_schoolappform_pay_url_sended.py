# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-01-25 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0020_auto_20191222_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappform',
            name='pay_url_sended',
            field=models.NullBooleanField(default=False),
        ),
    ]
