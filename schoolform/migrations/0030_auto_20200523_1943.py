# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-23 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0029_auto_20200523_1941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolappcurator',
            old_name='_instagramm',
            new_name='_instagram',
        ),
    ]
