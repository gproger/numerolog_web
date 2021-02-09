from rest_framework import serializers
from .models import PromoCode

class PromoCodesSerializer(serializers.ModelSerializer):

    flow = serializers.SerializerMethodField()


    def get_flow(self, obj):
        if obj.flow:
            return '{} {}'.format(obj.flow.flow, obj.flow.flow_name)
        else:
            return None
    class Meta:
        model = PromoCode
        exclude = ['evticket']


class PromoCodesTicketSerializer(serializers.ModelSerializer):

    evticket = serializers.SerializerMethodField()


    def get_evticket(self, obj):
        return '{} {}'.format(obj.evticket.id, obj.evticket.name)

    class Meta:
        model = PromoCode
        exclude = ['flow']
