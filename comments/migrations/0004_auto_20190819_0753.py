# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-19 07:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_cnt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='commentreply',
            options={'ordering': ['date']},
        ),
    ]
