from rest_framework import serializers
from .models import PromoCode

class PromoCodesSerializer(serializers.ModelSerializer):

    flow = serializers.SerializerMethodField()


    def get_flow(self, obj):
        return '{} {}'.format(obj.flow.flow, obj.flow.flow_name)

    class Meta:
        model = PromoCode
        fields = '__all__'


class PromoCodesTicketSerializer(serializers.ModelSerializer):

    event = serializers.SerializerMethodField()


    def get_event(self, obj):
        return '{} {}'.format(obj.event.id, obj.event.name)

    class Meta:
        model = PromoCode
        fields = '__all__'
