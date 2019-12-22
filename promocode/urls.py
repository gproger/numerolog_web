from django.conf.urls import url
from .views import PromoCodesListView


urls = [
    url(r'^numer/api/codes/', PromoCodesListView.as_view()),
]
