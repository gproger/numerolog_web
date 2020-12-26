from django.conf.urls import url
from .views import SchoolTrainingList
from .views import SchoolLessonList
from .views import SchoolTrainingDetailView

urls = [
    url(r'^numer/api/school/training/$', SchoolTrainingList.as_view()),
    url(r'^numer/api/school/training/(?P<id>[0-9]+)/$', SchoolTrainingDetailView.as_view()),
    url(r'^numer/api/school/lessons/$',SchoolLessonList.as_view()),
]
