from rest_framework import serializers
from .models import UserInfo
from utils.phone import get_phone


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField()
    first_name = serializers.CharField(min_length=2)
    last_name = serializers.CharField(min_length=2)
    middle_name = serializers.CharField(min_length=2)
    instagram = serializers.CharField(allow_blank=True)
    website = serializers.URLField(allow_blank=True)
    bid = serializers.DateField(format='%d.%m.%Y',input_formats=['%d.%m.%Y'])
    phone_valid = serializers.BooleanField(read_only=True)
    email_valid = serializers.BooleanField(read_only=True)

    def validate_phone(self, phone):
        return get_phone(phone)


class UserOrderTicketsListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.eventticket.event.name


class UserOrderSchoolListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return 'Обучение в школе на '+obj.flow.flow_name


class UserOrderCuratorListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return 'Услуга личного куратора' + obj.flow.flow_name


class UserOrderServicesListSerializer(serializers.Serializer):
    pass


class UserOrdersSerializer(serializers.Serializer):
    tickets = UserOrderTicketsListSerializer(many=True, source="ticket_set")
    school = UserOrderSchoolListSerializer(many=True, source="schoolappform_set")
    curator = UserOrderCuratorListSerializer(many=True, source="schoolappperscuratorform_set")

class UserOrderTicketSerializer(serializers.Serializer):
    pass

class UserOrderSchoolSerializer(serializers.Serializer):
    pass

class UserOrderCuratorSerializer(serializers.Serializer):
    pass

class UserOrderServicesSerializer(serializers.Serializer):
    pass
