# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-11-04 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20201104_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='order_num',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Номер услуги, отвечает за порядок отображения'),
            preserve_default=False,
        ),
    ]