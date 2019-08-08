from django.db import models

# Create your models here.

class SchoolAppFlow(models.Model):
    
    flow = models.PositiveIntegerField()

    def __str__(self):
        return str(self.flow)

class SchoolAppForm(models.Model):
     
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    bid = models.DateField()
    accepted = models.CharField(max_length=40)
    payed_by = models.CharField(max_length=240, blank=True, null=True)
    flow = models.ForeignKey(SchoolAppFlow)

    def save(self, *args, **kwargs):
        c_flow = SchoolAppFlow.objects.all().last()
        self.flow = c_flow
        print(args)
        print(kwargs)
        print("setted flow to")
        super(SchoolAppForm, self).save(*args, **kwargs)
