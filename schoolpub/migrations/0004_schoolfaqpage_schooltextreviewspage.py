# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-14 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import schoolpub.models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('schoolpub', '0003_auto_20200807_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolFAQPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('faq', wagtail.core.fields.StreamField([('faq', wagtail.core.blocks.ListBlock(schoolpub.models.FaqBlock, template='blocks/feedbackvideo_list.html'))], blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SchoolTextReviewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('feedbackReview', wagtail.core.fields.StreamField([('review', wagtail.core.blocks.ListBlock(schoolpub.models.FeedBackReviewIndexBlock, template='blocks/feedbackvideo_list.html'))], blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
