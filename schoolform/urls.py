from django.conf.urls import url
from .views import SchoolAppFormListView, SchoolAppFlowListView, SchoolAppFormCreateView, SchoolAppCuratorCreateView
from .views import SchoolAppFlowView, SchoolAppFlowRecruitmentListView
from .views import SchoolAppFormShowUpdateView
from .views import SchoolAppFormShowUpdateURLView
from .views import SchoolPersCuratorPayView
from .views import SchoolApplyPersCurator
from .views import SchoolApplyPersCuratorGetPayURL
from .views import SchoolAppFlowRegisterListView
from .views import SchoolAppFlowViewBySlug
from .views import FileSchoolServeView
from .views import SchoolAppFormUpdateFileUploadView
from .views import SchoolAppCuratorsListView
from .views import SchoolAppPersCuratorListView
from .views import SchoolAppDiscountsListAPView


urls = [
    url(r'^numer/api/flow/$', SchoolAppFlowListView.as_view()),
    url(r'^numer/api/fdesc/(?P<id>[0-9]+)/$',SchoolAppFlowView.as_view()),
    url(r'^numer/api/schoolflow/$', SchoolAppFormListView.as_view()),
    url(r'^numer/api/schooldiscounts/$', SchoolAppDiscountsListAPView.as_view()),
    url(r'^numer/api/curatorsflow/$', SchoolAppCuratorsListView.as_view()),
    url(r'^numer/api/perscurrflow/$', SchoolAppPersCuratorListView.as_view()),
#    url(r'^numer/api/schoolcurators', SchoolAppCuratorsListView.as_view()),
    url(r'^numer/api/addrecord/$', SchoolAppFormCreateView.as_view()),
    url(r'^numer/api/addcurator/$', SchoolAppCuratorCreateView.as_view()),
#    url(r'^numer/api/curator/(?P<id>[0-9]+)/$', SchoolPersCuratorPayView.as_view()),
    url(r'^numer/api/curator/(?P<id>[0-9]+)/$', SchoolApplyPersCurator.as_view()),
    url(r'^numer/api/curatorurl/(?P<id>[0-9]+)/$', SchoolApplyPersCuratorGetPayURL.as_view()),
#    url(r'^numer/api/curator_purl/(?P<id>[0-9]+)', SchoolApplyPersCuratorGetPayURL.as_view()),
    url(r'^numer/api/recr_flow/$', SchoolAppFlowRecruitmentListView.as_view()),
    url(r'^numer/api/recr_flow/(?P<slug__iexact>[-\w]+)/$', SchoolAppFlowViewBySlug.as_view()),
    url(r'^numer/api/reg_flow/$', SchoolAppFlowRegisterListView.as_view()),
    url(r'^numer/api/school/(?P<id>[0-9]+)/$', SchoolAppFormShowUpdateView.as_view()),
    url(r'^numer/api/schoolurl/(?P<id>[0-9]+)/$', SchoolAppFormShowUpdateURLView.as_view()),
    url('^schoolprivatefiles/(?P<pk>[0-9]+)/$', FileSchoolServeView.as_view(), name='file_download_school'),
    url(r'^numer/api/schoolupld/(?P<id>[0-9]+)/$', SchoolAppFormUpdateFileUploadView.as_view(), name='file_upload_school'),
]
