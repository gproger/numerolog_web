# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-23 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200523_1305'),
        ('schoolform', '0030_auto_20200523_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolappcurator',
            name='userinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserInfo'),
        ),
        migrations.AddField(
            model_name='schoolappform',
            name='userinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserInfo'),
        ),
        migrations.AddField(
            model_name='schoolappperscuratorform',
            name='userinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserInfo'),
        ),
    ]