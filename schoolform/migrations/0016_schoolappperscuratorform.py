# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-25 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_servicepage_short_descr'),
        ('django_tinkoff_merchant', '0004_auto_20191005_0630'),
        ('schoolform', '0015_auto_20191025_0625'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolAppPersCuratorForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('middle_name', models.CharField(max_length=40)),
                ('bid', models.DateField()),
                ('accepted', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('accepted_toss', models.ManyToManyField(to='blog.TermsOfServicePage')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolform.SchoolAppFlow')),
                ('payment', models.ManyToManyField(blank=True, null=True, to='django_tinkoff_merchant.Payment', verbose_name='Payment')),
            ],
        ),
    ]
