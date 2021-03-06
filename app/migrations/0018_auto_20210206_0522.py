# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2021-02-06 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_apporder_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='apporder',
            name='admincomment',
            field=models.TextField(blank=True, default='', verbose_name='Private Admin Comments'),
        ),
        migrations.AddField(
            model_name='apporder',
            name='expertcomment',
            field=models.TextField(blank=True, default='', verbose_name='Private expert Comments'),
        ),
        migrations.AlterField(
            model_name='apporder',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='User Order Comments'),
        ),
    ]
