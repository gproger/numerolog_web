# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-11-04 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_servicepage_whatinclude'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='bgColor',
            field=models.CharField(blank=True, max_length=255, verbose_name='Цвет подложки'),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='textColor',
            field=models.CharField(blank=True, max_length=255, verbose_name='Цвет текста'),
        ),
    ]
