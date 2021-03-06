# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-18 06:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('blog', '0013_auto_20200201_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='image_dark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='image_light',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
