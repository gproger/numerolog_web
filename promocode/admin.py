from django.contrib import admin
from .models import PromoCode

# Register your models here.

def flow_name(obj):
    if obj.flow is not None:
        return '{}'.format(obj.flow.flow_name)

def flow_auth(obj):
    return '{}'.format(obj.flow.avail_by_code)

def event_tick(obj):
    if obj.evticket is not None:
        return '{}'.format(obj.evticket.name)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = [event_tick, flow_name, flow_auth, 'code', 'is_percent', 'discount',
                    'elapsed_count', 'emitter','created_at']
    list_filter = ['emitter', 'is_percent',
                    'flow__flow_name', 'evticket__name','flow__avail_by_code', 'discount',
                    'elapsed_count','created_at']
