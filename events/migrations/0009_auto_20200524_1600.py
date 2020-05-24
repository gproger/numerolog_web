# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-24 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200523_1305'),
        ('events', '0008_auto_20200507_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='email',
            new_name='_email',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='first_name',
            new_name='_first_name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='last_name',
            new_name='_last_name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='middle_name',
            new_name='_middle_name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='phone',
            new_name='_phone',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='phone_valid',
            new_name='_phone_valid',
        ),
        migrations.AddField(
            model_name='ticket',
            name='userinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserInfo'),
        ),
    ]
