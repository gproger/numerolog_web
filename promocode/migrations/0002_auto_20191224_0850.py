# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-12-24 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0020_auto_20191222_1429'),
        ('promocode', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocode',
            name='price',
        ),
        migrations.AddField(
            model_name='promocode',
            name='price',
            field=models.ManyToManyField(blank=True, null=True, to='schoolform.PriceField'),
        ),
    ]
