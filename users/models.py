from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class UserInfo(models.Model):
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20,blank=True)
    first_name = models.CharField(max_length=40,blank=True)
    last_name = models.CharField(max_length=40,blank=True)
    middle_name = models.CharField(max_length=40,blank=True)
    instagram = models.CharField(max_length=80,blank=True)
    website = models.URLField(null=True, blank=True)
    bid = models.DateField(null=True,blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, related_name="ninfo",null=True, blank=True)
    phone_valid = models.NullBooleanField(default=False)
    email_valid = models.NullBooleanField(default=False)
    validating_email = models.NullBooleanField(default=False)
    email_validation_code = models.IntegerField(null=True)
    email_temp = models.EmailField(blank=True)
    
### this class used as user info for auth user
### every application in system must be linked to this userinfo

### all SchoolForms
    @property
    def is_correct(self):
        if self.user is None:
            return False
        if self.bid is None:
            return False
        
        if self.middle_name is None:
            return False
        if len(self.middle_name) < 2:
            return False
        
        if self.first_name is None:
            return False
        if len(self.first_name) < 2:
            return False

        if self.last_name is None:
            return False
        if len(self.last_name) < 2:
            return False

        if self.phone is None:
            return False
        if self.email is None:
            return False

        return True

    @property
    def is_validated(self):
        return self.phone_valid and self.email_valid

    def send_email_code(self):
        send_task('users.tasks.send_email_code',
                kwargs={"userInfo_id": self.pk})



    

class UserReviews(models.Model):
    pass


