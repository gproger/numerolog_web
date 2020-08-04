# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-04 06:24
from __future__ import unicode_literals

from django.db import migrations
import schoolpub.models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schoolpub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoollandingpage',
            name='feedback',
            field=wagtail.core.fields.StreamField([('video', wagtail.core.blocks.ListBlock(schoolpub.models.FeedBackVideo))], blank=True, null=True),
        ),
    ]
