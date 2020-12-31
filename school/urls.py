from django.conf.urls import url
from .views import SchoolTrainingList
from .views import SchoolTrainingCreateCopyView
from .views import SchoolLessonList
from .views import SchoolTrainingDetailView
from .views import SchoolLessonDetailView

urls = [
    url(r'^numer/api/school/training/$', SchoolTrainingList.as_view()),
    url(r'^numer/api/school/trainingc/$', SchoolTrainingCreateCopyView.as_view()),
    url(r'^numer/api/school/training/(?P<id>[0-9]+)/$', SchoolTrainingDetailView.as_view()),
    url(r'^numer/api/school/lessons/$',SchoolLessonList.as_view()),
    url(r'^numer/api/school/lessons/(?P<id>[0-9]+)/$', SchoolLessonDetailView.as_view()),
]
