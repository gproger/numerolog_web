from django.conf.urls import url
from .views import PromoCodesListView, PromoCodesCreate


urls = [
    url(r'^numer/api/codes/', PromoCodesListView.as_view()),
    url(r'^numer/api/crcodes/', PromoCodesCreate.as_view()),
]
