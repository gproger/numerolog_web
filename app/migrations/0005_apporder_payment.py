# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-22 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_tinkoff_merchant', '0004_auto_20191005_0630'),
        ('app', '0004_appuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='apporder',
            name='payment',
            field=models.ManyToManyField(blank=True, null=True, to='django_tinkoff_merchant.Payment', verbose_name='Payment'),
        ),
    ]