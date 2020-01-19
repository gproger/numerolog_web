# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-01-07 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SendedSMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=30, verbose_name='Phone Number')),
                ('text', models.TextField(verbose_name='Message text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time created')),
                ('sended_at', models.DateTimeField(auto_now=True, verbose_name='Last time sended')),
                ('unique_id', models.CharField(max_length=40, verbose_name='Message ID')),
                ('debug_result', models.TextField(verbose_name='Debug message result from API')),
                ('status', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SMSSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_text', models.TextField(verbose_name='Template code text')),
                ('expert', models.TextField(verbose_name='Template expert notify')),
                ('client_st', models.TextField(verbose_name='Template client notify service start')),
                ('client_ready', models.TextField(verbose_name='Template client notify service ready')),
            ],
        ),
        migrations.CreateModel(
            name='NotifySMS',
            fields=[
                ('sendedsms_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='smsgate.SendedSMS')),
            ],
            bases=('smsgate.sendedsms',),
        ),
        migrations.CreateModel(
            name='PhoneAuthSMS',
            fields=[
                ('sendedsms_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='smsgate.SendedSMS')),
                ('code', models.PositiveIntegerField()),
            ],
            bases=('smsgate.sendedsms',),
        ),
    ]
