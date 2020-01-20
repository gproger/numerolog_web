from django.conf.urls import url
from .views import OfflineEventListView, OfflineEventRUDView
from .views import EventTicketTemplateListView, EventTicketTemplateRUDView
from .views import TicketListView, TicketAddView



urls = [
    url(r'^numer/api/events/$', OfflineEventListView.as_view()),
    url(r'^numer/api/events/(?P<id>[0-9]+)/$',OfflineEventRUDView.as_view()),
    url(r'^numer/api/events/(?P<event>[0-9]+)/eventticket/$', EventTicketTemplateListView.as_view()),
#    url(r'^numer/api/schoolcurators', SchoolAppCuratorsListView.as_view()),
    url(r'^numer/api/events/(?P<event>[0-9]+)/eventticket/(?P<id>[0-9]+)/$', EventTicketTemplateRUDView.as_view()),
    url(r'^numer/api/events/(?P<event>[0-9]+)/tickets', TicketListView.as_view()),
    url(r'^numer/api/events/ticket/$', TicketAddView.as_view()),
    url(r'^numer/api/actevents', OfflineActiveEventView.as_view()),

]
