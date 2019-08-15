from django.db import models

# Create your models here.

class SchoolAppFlow(models.Model):
    STATES = (
        (0, "created"),
        (1, "recruitment"),
        (2, "register"),
        (3, "started"),
        (4, "finished")
    )

    flow = models.PositiveIntegerField()
    state = models.IntegerField(choices=STATES, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.flow)

class SchoolAppForm(models.Model):
     
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    instagramm = models.CharField(max_length=80)
    bid = models.DateField()
    accepted = models.CharField(max_length=40)
    payed_by = models.CharField(max_length=240, blank=True, null=True)
    flow = models.ForeignKey(SchoolAppFlow)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        c_flow = SchoolAppFlow.objects.all().last()
        self.flow = c_flow
        print(args)
        print(kwargs)
        print("setted flow to")
        super(SchoolAppForm, self).save(*args, **kwargs)
