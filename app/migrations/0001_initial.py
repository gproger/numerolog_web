# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-31 12:12
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('deadline_at', models.DateTimeField()),
                ('consult_at', models.DateTimeField()),
                ('items', django.contrib.postgres.fields.jsonb.JSONField()),
                ('doer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.PositiveIntegerField()),
                ('registered', models.BooleanField(default=False)),
                ('code_time', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='apporder',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.AppUser'),
        ),
    ]
