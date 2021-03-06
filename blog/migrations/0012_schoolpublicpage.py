# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-12-15 04:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('blog', '0011_servicepage_short_descr'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolPublicPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('html', wagtail.core.fields.RichTextField(blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Page date')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
