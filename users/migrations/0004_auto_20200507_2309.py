# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-07 23:09
from __future__ import unicode_literals

from django.db import migrations

from django.apps import apps as global_apps



def forwards(apps, schema_editor):
    try:
        SchoolAppCuratorModel = apps.get_model('schoolform', 'SchoolAppCurator')
    except LookupError:
        # The old app isn't installed.
        return

    UserInfoModel = apps.get_model('users', 'UserInfo')

    list_emails = UserInfoModel.objects.all().values_list('email', flat=True)

    queryset = SchoolAppCuratorModel.objects.exclude(email__in=list_emails).order_by('email')
    last_email = ''
    list_t = []
    ### iterate through models and skip duplicate
    for obj in queryset:
        if last_email != obj.email:
            new_obj = UserInfoModel(email=obj.email,
            phone=obj.phone,
            first_name=obj.first_name,
            last_name=obj.last_name,
            middle_name=obj.middle_name,
            instagram=obj.instagramm,
            bid=obj.bid,
            phone_valid=obj.phone_valid)
            last_email=obj.email
            list_t.append(new_obj)
        elif obj.phone_valid:
            list_t[-1].phone_valid=obj.phone_valid
        
    #create list of object by one query
    UserInfoModel.objects.bulk_create(
        list_t
    )

 #   NewModel.objects.bulk_create(
 #       NewModel(new_attribute=old_object.old_attribute)
 #       for old_object in OldModel.objects.all()
 #   )

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200507_2242'),
    ]

    if global_apps.is_installed('schoolform'):
        dependencies.append(('schoolform', '0027_schoolappflow_is_hidden'))

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
