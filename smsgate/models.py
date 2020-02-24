from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils.timezone import utc
# Create your models here.

class SMSSettings(models.Model):
    code_text = models.TextField(verbose_name=_("Template code text"))
    expert = models.TextField(verbose_name=_("Template expert notify"))
    client_st = models.TextField(verbose_name=_("Template client notify service start"))
    client_ready = models.TextField(verbose_name=_("Template client notify service ready"))


class SendedSMS(models.Model):
    phone = models.CharField(max_length=30,verbose_name=_("Phone Number"))
    text = models.TextField(verbose_name=_("Message text"))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_("Time created"))
    sended_at = models.DateTimeField(auto_now=True, verbose_name=_("Last time sended"))
    unique_id = models.CharField(max_length=40,verbose_name=_("Message ID"))
    debug_result = models.TextField(verbose_name=_("Debug message result from API"))
    status = models.PositiveSmallIntegerField(default=0)

    def get_time_delta(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return (now - self.sended_at).total_seconds()

class PhoneAuthSMS(SendedSMS):
    code = models.PositiveIntegerField()
    type = models.CharField(max_length=200,blank=True)
    t_id = models.PositiveIntegerField()

class NotifySMS(SendedSMS):
    pass
