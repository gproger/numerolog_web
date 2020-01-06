from django.contrib import admin
from .models import PromoCode

# Register your models here.

def flow_name(obj):
    return '{}'.format(obj.flow.flow_name)

def flow_auth(obj):
    return '{}'.format(obj.flow.avail_by_code)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = [flow_name, flow_auth, 'code', 'is_percent', 'discount',
                    'elapsed_count', 'emitter','created_at']
    list_filter = ['emitter', 'is_percent',
                    'flow__flow_name', 'flow__avail_by_code', 'discount',
                    'elapsed_count','created_at']
