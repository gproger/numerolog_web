from django.db import models
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


class FeedBackVideo(blocks.StructBlock):
    title = blocks.CharBlock()
    url = blocks.URLBlock()

    class Meta:
        label='Видео отзывы'
        template='blocks/feedbackvideo_item.html'


class SchoolLandingPage(Page):

    feedback = StreamField([('video',blocks.ListBlock(FeedBackVideo, template='blocks/feedbackvideo_list.html'))],null=True,blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('feedback', classname="full")
    ]


# Create your models here.
