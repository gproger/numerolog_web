# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-31 10:44
from __future__ import unicode_literals

from django.db import migrations

def forwards(apps, schema_editor):

    SchoolAppPersCuratorForm = apps.get_model('schoolform','SchoolAppPersCuratorForm')


    query = SchoolAppPersCuratorForm.objects.all()

    for obj in query:
        obj.price = obj.flow.pers_cur_price
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('schoolform', '0034_schoolappperscuratorform_price'),
    ]

    operations = [
         migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
