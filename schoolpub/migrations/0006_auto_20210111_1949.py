# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2021-01-11 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolpub', '0005_auto_20200814_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoollandingpage',
            name='link_1_2_stage',
            field=models.URLField(default='/', verbose_name='Ссылка на 1 и 2 ступень'),
        ),
        migrations.AddField(
            model_name='schoollandingpage',
            name='link_1_stage',
            field=models.URLField(default='/', verbose_name='Ссылка на 1 ступень'),
        ),
        migrations.AddField(
            model_name='schoollandingpage',
            name='link_2_stage',
            field=models.URLField(default='/', verbose_name='Ссылка на 2 ступень'),
        ),
    ]
