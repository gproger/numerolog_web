# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-09-20 17:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_appautogeneratoroptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apporder',
            name='doer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='serv_appl_doer', to=settings.AUTH_USER_MODEL),
        ),
    ]
