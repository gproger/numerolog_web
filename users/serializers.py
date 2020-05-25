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


class UserOrderSerializer():
    pass

class UserOrderTicketsListSerializer():
    pass

class UserOrderSchoolListSerializer():
    pass

class UserOrderCuratorListSerializer():
    pass

class UserOrderServicesListSerializer():
    pass

class UserOrderTicketSerializer():
    pass

class UserOrderSchoolSerializer():
    pass

class UserOrderCuratorSerializer():
    pass

class UserOrderServicesSerializer():
    pass
