from django.conf.urls import url
from .views import PromoCodesListView, PromoCodesCreate, PromoCodesTest, PromoTicketCodesTestTicket


urls = [
    url(r'^numer/api/codes/', PromoCodesListView.as_view()),
    url(r'^numer/api/crcodes/', PromoCodesCreate.as_view()),
    url(r'^numer/api/tcodes/', PromoCodesTest.as_view()),
    url(r'^numer/api/tickcodes/', PromoTicketCodesTestTicket.as_view()),
]
