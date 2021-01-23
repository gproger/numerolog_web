from django.conf.urls import url

from .views import UserInfoDetail
from .views import UserInfoValidateTest
from .views import UserInfoValidateSend
from .views import UserOrderList
from .views import UserOrderTicketList
from .views import UserOrderSchoolList
from .views import UserOrderCuratorList
from .views import UserOrderServicesList
from .views import UserOrderTicketDetail
from .views import UserOrderSchoolDetail
from .views import UserOrderCuratorDetail
from .views import UserOrderServicesDetail
from .views import UserWorksList
from .views import UserOfferList

urls = [
    url(r'^numer/api/user/$', UserInfoDetail.as_view(), name="users:info"),
    url(r'^numer/api/user/validate/test/$', UserInfoValidateTest.as_view(), name="users:validate:test"),
    url(r'^numer/api/user/validate/send/$', UserInfoValidateSend.as_view(), name="users:validate:send"),
    url(r'^numer/api/user/works/$',UserWorksList.as_view(), name="users:works"),
    url(r'^numer/api/user/orders/$',UserOrderList.as_view(), name="users:orders"),
    url(r'^numer/api/user/offers/$',UserOfferList.as_view(), name="users:offers"),
    url(r'^numer/api/user/orders/ticket/$', UserOrderTicketList.as_view(), name="users:orders:tickets"),
    url(r'^numer/api/user/orders/school/$', UserOrderSchoolList.as_view(), name="users:orders:schools"),
    url(r'^numer/api/user/orders/curator/$', UserOrderCuratorList.as_view(), name="users:orders:curators"),
    url(r'^numer/api/user/orders/services/$', UserOrderServicesList.as_view(), name="users:orders:services"),
    url(r'^numer/api/user/orders/ticket/(?P<id>[0-9]+)/$', UserOrderTicketDetail.as_view(), name="users:orders:ticket"),
    url(r'^numer/api/user/orders/school/(?P<id>[0-9]+)/$', UserOrderSchoolDetail.as_view(), name="users:orders:school"),
    url(r'^numer/api/user/orders/curator/(?P<id>[0-9]+)/$', UserOrderCuratorDetail.as_view(), name="users:orders:curator"),
    url(r'^numer/api/user/orders/services/(?P<id>[0-9]+)/$', UserOrderServicesDetail.as_view(), name="users:orders:service"),
]
