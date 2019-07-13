from django.db import models

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
class SimpleCalcPage(Page):
    description = models.CharField(max_length=255, blank=True,)
    body = RichTextField(blank=True)
    template = 'simple_calc_page.html'

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('body',classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        return context

# Create your models here.
