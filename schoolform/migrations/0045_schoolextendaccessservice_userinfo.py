# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-12-31 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200529_0342'),
        ('schoolform', '0044_schoolextendaccessservice_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolextendaccessservice',
            name='userinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='schoolextend', to='users.UserInfo'),
        ),
    ]