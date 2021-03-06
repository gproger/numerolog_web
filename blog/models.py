# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from datetime import date

from django import forms
from django.db import models
from django.http import Http404, HttpResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format

import wagtail
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtail.search import index

#from blog.blocks import TwoColumnBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from comments.serializers import CommentBlogSerializer
#from wagtailmd.utils import MarkdownField, MarkdownPanel


class BlogPage(RoutablePageMixin, Page):
    description = models.CharField(max_length=255, blank=True,)

    api_fields = [
        APIField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    def get_posts(self):
        return PostPage.objects.descendant_of(self).live().order_by('-date')

#    @route(r'^(\d{4})/$')
#    @route(r'^(\d{4})/(\d{2})/$')
#    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(date__year=year)
        self.search_type = 'date'
        self.search_term = year
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

#    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)

#    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

#    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)

#    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)


#    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)


class PostPage(Page):
#    body = MarkdownField()
    body = RichTextField(blank=True)
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
#    excerpt = MarkdownField(
#        verbose_name='excerpt', blank=True,
#    )

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)

    search_fields = Page.search_fields + [ # Inherit search_fields from Page
        index.SearchField('body', partial_match=True, boost=3),
        index.RelatedFields('tags', [
                index.SearchField('name', partial_match=True, boost=10),
            ]),
#        index.SearchField('tags'),
#        index.SearchField('categories'),
#        index.FilterField('tags'),
#        index.FilterField('categories'),
        index.FilterField('date'),
    ]

    api_fields = [
        APIField('body'),
        APIField('date'),
        APIField('header_image'),
        APIField('categories'),
        APIField('tags'),
	APIField('comments',serializer=CommentBlogSerializer)
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body',classname='full'),
#        MarkdownPanel("body"),
#        MarkdownPanel("excerpt"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        context['post'] = self
        return context

    def save(self, *args, **kwargs):
        super(PostPage,self).save(*args, **kwargs)


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    def get_form_fields(self):
        return self.custom_form_fields.all()

    @property
    def blog_page(self):
        return self.get_parent().specific


class ServiceAboutBlock(blocks.StructBlock):
    desc = blocks.CharBlock()
    image = ImageChooserBlock()

    class Meta:
        label='???????????????? ????????????'
        template='blocks/feedbackvideo_item.html'

class ServicePage(Page):
    price = models.PositiveIntegerField(blank=True)
    expert = models.BooleanField(blank=True)

    date_cnt = models.SmallIntegerField(blank=True)

    whatInclude = models.CharField(max_length=255, blank=True)

    date = models.DateTimeField(verbose_name="Service Added", default=datetime.datetime.today)

    toss = ParentalManyToManyField(
        'blog.TermsOfServicePage',
        null=True,
        blank=True,
        related_name='related_services',
        verbose_name='???????????????????? ?? ????????????????',
	)


    adult_cnt = models.SmallIntegerField(blank=True, default = 0, verbose_name="???????????????? ?? ??????????????")
    kids_cnt = models.SmallIntegerField(blank=True, default = 0, verbose_name="?????????? ?? ??????????????")
    comp_parent = models.NullBooleanField(blank=True, default=False, verbose_name="?????????????????????????? ??????????????????")
    impr_chld = models.NullBooleanField(blank=True, default=False, verbose_name="?????????????? ???? ??????????????")


    bgColor = models.CharField(max_length=255, blank=True, verbose_name="???????? ????????????????")
    textColor = models.CharField(max_length=255, blank=True, verbose_name="???????? ????????????")
    order_num = models.SmallIntegerField(blank=True, verbose_name="?????????? ????????????, ???????????????? ???? ?????????????? ??????????????????????")

    image_light = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    image_dark = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    about = StreamField([('about',blocks.ListBlock(ServiceAboutBlock, template='blocks/feedbackvideo_list.html'))],null=True,blank=True)


    search_fields = Page.search_fields + [ # Inherit search_fields from Page
        index.SearchField('title', partial_match=True, boost=3),
        index.FilterField('expert'),
    ]

    api_fields = [
        APIField('title'),
        APIField('price'),
        APIField('expert'),
        APIField('date_cnt'),
        APIField('image_light'),
        APIField('image_dark'),
        APIField('about'),
        APIField('whatInclude')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('whatInclude',classname='full'),
        FieldPanel('price',classname='full'),
        FieldPanel('expert',classname='full'),
        FieldPanel('date_cnt',classname='full'),
        FieldPanel('toss', widget=forms.CheckboxSelectMultiple),
        FieldPanel('adult_cnt',classname='full'),
        FieldPanel('kids_cnt',classname='full'),
        FieldPanel('comp_parent',classname='full'),
        FieldPanel('impr_chld',classname='full'),
        FieldPanel('bgColor',classname='full'),
        FieldPanel('textColor',classname='full'),
        FieldPanel('order_num',classname='full'),
        ImageChooserPanel('image_light'),
        ImageChooserPanel('image_dark'),
        StreamFieldPanel('about', classname="full")
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific


class TermsOfServicePage(Page):
    descr = RichTextField(blank=True)

    date = models.DateTimeField(verbose_name="Service Added", default=datetime.datetime.today)

    content_panels = Page.content_panels + [
        FieldPanel('descr',classname='full'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific


class SchoolPublicPage(Page):
    html = RichTextField(blank=True)

    date = models.DateTimeField(verbose_name="Page date", default=datetime.datetime.today)

    content_panels = Page.content_panels + [
        FieldPanel('html',classname='full'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific
