# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-24 16:04
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    UserInfoModel = apps.get_model('users', 'UserInfo')
    Ticket = apps.get_model('events','Ticket')

    queryset = Ticket.objects.all()

    for ticket in queryset:
        u_info = UserInfoModel.objects.filter(phone=ticket._phone)
        if u_info.first() is not None:
            ticket.userinfo = u_info.first()
            ticket.save()
        else:
            u_info = UserInfoModel.objects.filter(email=ticket._email)
            if u_info.first() is not None:
                ticket.userinfo = u_info.first()
                ticket.save()
            else:
                u_info = UserInfoModel(
                email=ticket._email,
                phone=ticket._phone,
                first_name=ticket._first_name,
                middle_name=ticket._middle_name,
                last_name=ticket._last_name,
                )
                u_info.save()
                ticket.userinfo = u_info
                ticket.save()
        


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20200524_1600'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
