from rest_framework import serializers
from .models import UserInfo
from utils.phone import get_phone


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    email_temp = serializers.EmailField(read_only=True)
    phone = serializers.CharField(read_only=True)
    first_name = serializers.CharField(min_length=2)
    last_name = serializers.CharField(min_length=2)
    middle_name = serializers.CharField(min_length=2)
    instagram = serializers.CharField(allow_blank=True)
#    website = serializers.URLField(required=False, allow_blank=True)
    bid = serializers.DateField(format='%d.%m.%Y',input_formats=['%d.%m.%Y'])
    phone_valid = serializers.BooleanField(read_only=True)
    email_valid = serializers.BooleanField(read_only=True)
    validate_url = serializers.SerializerMethodField()
    validating_email = serializers.BooleanField(read_only=True)
    
    def validate_phone(self, phone):
        return get_phone(phone)

    def get_validate_url(self, obj):
        if obj.is_validated and obj.is_correct:
            return None
        return '/numer/api/user'

    def update(self, instance, validated_data):

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
        return '???????????????? ?? ?????????? ???? '+obj.flow.flow_name


class UserOrderSchoolExtendListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return '?????????????????? ?????????????? ?? ???????????????????? ???????????????? ???? '+obj.form.flow.flow_name


class UserOrderCuratorListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return '???????????? ?????????????? ???????????????? ' + obj.flow.flow_name


class UserOrderServicesListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True,format="%d.%m.%Y %H:%M")
    title = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        if hasattr(obj,'name') and obj.name is not None:
            return obj.name
        return '???????????? '+str(obj.id)


class UserOrdersSerializer(serializers.Serializer):
    ticket = UserOrderTicketsListSerializer(many=True, source="ticket_set")
    school = UserOrderSchoolListSerializer(many=True, source="schoolappform_set")
    curator = UserOrderCuratorListSerializer(many=True, source="schoolappperscuratorform_set")
    service  = UserOrderServicesListSerializer(many=True, source="user.serv_appl_owner")
    schoolextend = UserOrderSchoolExtendListSerializer(many=True)

class UserOrderTicketSerializer(serializers.Serializer):
    pass

class UserOrderSchoolSerializer(serializers.Serializer):
    pass

class UserOrderCuratorSerializer(serializers.Serializer):
    pass

class UserOrderServicesSerializer(serializers.Serializer):
    pass

class UserWorkSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    payed_amount = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    deadline_at = serializers.DateTimeField(read_only=True)
    consult_at = serializers.DateTimeField(read_only=True)
    requester = serializers.SerializerMethodField()
    payed_amount = serializers.IntegerField(read_only=True)
    pended = serializers.SerializerMethodField(read_only=True)

    def get_requester(self, obj):
        if hasattr(obj.owner,'ninfo') and obj.owner.ninfo is not None:
            return obj.owner.ninfo.first_name
        else:
            return obj.owner.get_real_name()

    def get_pended(self,obj):
        if not hasattr(obj,'workstate'):
            return False
        if not 'assign' in obj.workstate:
            return False
        if not hasattr(self.context['request'].user,'expert_rec'):
            return False
        if self.context['request'].user.expert_rec is None:
            return False
        exp_id = self.context['request'].user.expert_rec.pk
        for item in obj.workstate['assign']:
            if item['exp_id'] == exp_id and item['confirmed'] == False and item['pending']== True:
                return True
        return False
