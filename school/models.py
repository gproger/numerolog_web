from django.db import models
from schoolform.models import SchoolAppCurator
from schoolform.models import SchoolAppFlow



# Create your models here.


class SchoolTraining(models.Model):
    curators = models.ManyToManyField(SchoolAppCurator, related_name='active_training')
    flow = models.ForeignKey(SchoolAppFlow,related_name='trainings')
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} {}'.format(self.flow.flow_name, self.name)

class SchoolLesson(models.Model):
    training = models.ForeignKey(SchoolTraining, related_name='lessons')
    name = models.CharField(max_length=250)
    descr = models.TextField(blank=True)
    time_start = models.DateTimeField()
    has_homework = models.BooleanField(default=False)
    homework_html = models.TextField(blank=True)
    lesson_content = models.TextField(blank=True)


