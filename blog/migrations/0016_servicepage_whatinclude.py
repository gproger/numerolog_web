# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-26 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20200826_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='whatInclude',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
