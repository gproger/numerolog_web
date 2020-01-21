from django.conf.urls import url
from .views import PromoCodesListView, PromoCodesCreate, PromoCodesTest, PromoTicketCodesTestTicket
from .views import PromoTicketCodesListView, PromoTicketCodesCreate

urls = [
    url(r'^numer/api/codes/', PromoCodesListView.as_view()),
    url(r'^numer/api/crcodes/', PromoCodesCreate.as_view()),
    url(r'^numer/api/tcodes/', PromoCodesTest.as_view()),

    url(r'^numer/api/ticktestcodes/', PromoTicketCodesTestTicket.as_view()),
    url(r'^numer/api/tickcodes/', PromoTicketCodesListView.as_view()),
    url(r'^numer/api/crtickcodes/', PromoTicketCodesCreate.as_view()),

]
