# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-01-20 22:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200120_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='middlename',
            new_name='middle_name',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='secondname',
            new_name='second_name',
        ),
    ]
