from rest_framework import serializers
from .models import SchoolAppForm, SchoolAppFlow, SchoolAppCurator, SchoolAppPersCuratorForm, SchoolDiscount
from .models import SchoolExtendAccessService
from django_tinkoff_merchant.serializers import PaymentSerializer

from users.serializers import UserInfoSerializer
from utils.phone import get_phone
from django.urls import reverse
from dateutil.relativedelta import *


class SchoolAppFormCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value

    def validate_phone(self, value):
        get_phone(value)

    class Meta:
        model = SchoolAppForm
        exclude = ['payment']


class SchoolAppCuratorCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    flow = serializers.PrimaryKeyRelatedField(queryset=SchoolAppFlow.objects.all(),many=False)


    def validate_email(self, value):
        norm_value = value.lower()
        return norm_value


    class Meta:
        model = SchoolAppCurator
        fields = '__all__'

class SchoolAppFlowListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'],required=False)

    def get_state(self, obj):
        return obj.get_state_display()

    class Meta:
        model = SchoolAppFlow
        fields = ['state','created','flow','flow_name','id']


class SchoolAppFlowSerializer(serializers.ModelSerializer):
#    state = serializers.SerializerMethodField()
    state = serializers.ChoiceField(choices=SchoolAppFlow.STATES)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    choices = serializers.SerializerMethodField()
    slug = serializers.SlugField( allow_unicode=True)

    def get_choices(self, obj):
        return SchoolAppFlow.STATES

    def get_state(self, obj):
        return obj.get_state_display()


    class Meta:
        model = SchoolAppFlow
        fields = '__all__'


class SchoolAppFlowWOChoicesSerializer(serializers.ModelSerializer):

#    state = serializers.SerializerMethodField()
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    toss = serializers.SerializerMethodField()
    cur_toss = serializers.SerializerMethodField()
    pers_toss = serializers.SerializerMethodField()

    slug = serializers.SlugField(required = False)

    def get_cur_toss(self,obj):
        lis = []
        for x in obj.cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_toss(self,obj):
        lis = []
        for x in obj.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_pers_toss(self, obj):
        lis = []
        for x in obj.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis


    class Meta:
        model = SchoolAppFlow
        fields = '__all__'


class SchoolAppFlowWOChoicesSerializerBySlug(serializers.ModelSerializer):

#    state = serializers.SerializerMethodField()
    price = serializers.IntegerField(default=30000, required = False)

#   recruitment fields
    recruitment_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    recruitment_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

#   started fields
    education_start = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    education_stop = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)

    toss = serializers.SerializerMethodField()
    cur_toss = serializers.SerializerMethodField()
    pers_toss = serializers.SerializerMethodField()

    ninfo = serializers.SerializerMethodField()

    discount = serializers.SerializerMethodField()

    def get_ninfo(self, obj):
        uinfo = self.context.get('request').user.ninfo
        return UserInfoSerializer(uinfo).data

    

    def get_cur_toss(self,obj):
        lis = []
        for x in obj.cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_toss(self,obj):
        lis = []
        for x in obj.toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_pers_toss(self, obj):
        lis = []
        for x in obj.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return lis

    def get_discount(self, obj):
        max_discount = 0
        uinfo = self.context.get('request').user.ninfo
        forms = SchoolAppForm.objects.filter(userinfo=uinfo)
        all_discounts = obj.discounts_by_orders.all()
        for form in forms:
            if form.payed_amount != form.price:
                continue
            for t in all_discounts:
                if t.flow == form.flow:
                    if t.discount > max_discount:
                        max_discount = t.discount
        return max_discount
            


    class Meta:
        model = SchoolAppFlow
        lookup_field = 'slug'
        fields = '__all__'


class SchoolAppFormFlowStudentsList(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)
    bid = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y'] , required = False)
    payment = PaymentSerializer(required=False, many = True)
    price_f = serializers.SerializerMethodField()
    promocode = serializers.SerializerMethodField()

    def get_price_f(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.price
            else:
                return obj.price
        else:
            return obj.price

    def get_promocode(self, obj):
        if hasattr( obj, 'price_f'):
            if obj.price_f is not None:
                return obj.price_f.promocode_set.all()[0].code
            else:
                return ''
        else:
            return ''


    def get_amount(self,obj):
        total = 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        return total/100

    class Meta:
        model = SchoolAppForm
        fields = ['first_name','middle_name','last_name','bid','phone','email','instagramm','created','payed_by','amount','payment','price','price_f','promocode','phone_valid','payed_amount']

class SchoolPersCuratorSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(required=False, many = True)
    amount = serializers.SerializerMethodField(required=False)
    order = serializers.SerializerMethodField(required=False)



    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order

        toss = []

        for x in obj.accepted_toss.all():
            toss.append({'url': '/tos/'+str(x.id),'title' : x.title})

        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.flow.flow_name, 'type' : 'flow_name'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})
        order.append({'name' : 'Соглашения:', 'value' : toss, 'type' : 'toss'})
        #if hasattr(obj,'payed_outline'):
        #    if obj.payed_outline > 0:
        #        order.append({'name' : 'Предоплата:', 'value' : obj.payed_outline})

        #    order.append({'name' : 'Оплачено на карту:', 'value' : obj.payed_outline})
        #if hasattr(obj,'payed_by'):
        #    if obj.payed_by != '':
        #        order.append({'name' : 'Оплачено от имени:', 'value' : obj.payed_by})

        return order

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100


    class Meta:
        model = SchoolAppPersCuratorForm
        exclude = ['flow']


class SchoolAppFormSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(required=False)

    payment = PaymentSerializer(required=False, many = True)

    amount = serializers.SerializerMethodField()

    cform = SchoolPersCuratorSerializer(required=False, many=False, read_only=True, source="get_curator_form")

    curator = serializers.SerializerMethodField(required=False)

    phone_valid = serializers.BooleanField(required=False)

    cancelUrl = serializers.SerializerMethodField(required=False)

    uploadDocumentUrl = serializers.SerializerMethodField(required=False)

    files = serializers.SerializerMethodField(required=False)


    saleUrl  = serializers.SerializerMethodField(required=False)

    prolong = serializers.SerializerMethodField()

    flow_id = serializers.SerializerMethodField()

    buyCreditURL = serializers.SerializerMethodField(required=False)

    credit = serializers.SerializerMethodField()

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order
        toss = []

        for x in obj.accepted_toss.all():
            toss.append({'url': '/tos/'+str(x.id),'title' : x.title})


        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.flow.flow_name, 'type' : 'flow_name'})

        date_started = obj.flow.education_start
        date_started = '{}.{}.{}'.format(date_started.day,date_started.month, date_started.year)
        date_end = obj.flow.education_stop
        date_end = '{}.{}.{}'.format(date_end.day,date_end.month, date_end.year)
        order.append({'name' : 'Начало обучения:', 'value' : date_started, 'type' : 'date_start'})
        order.append({'name' : 'Окончание обучения:', 'value' : date_end, 'type' : 'date_end'})

        date_access = obj.flow.education_stop
        date_access = date_access + relativedelta(months=+6)

        if hasattr(obj,'access_till') and obj.access_till is not None:
            date_access = obj.access_till

        date_access = '{}.{}.{}'.format(date_access.day,date_access.month, date_access.year)

        order.append({'name' : 'Доступ к материалам до:', 'value' : date_access, 'type' : 'date_access'})
        order.append({'name' : 'Фамилия:', 'value' : obj.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость обучения:', 'value' : obj.price, 'type' : 'price'})
        order.append({'name' : 'Соглашения:', 'value' : toss, 'type' : 'toss'})
	#if hasattr(obj,'payed_outline'):
        #    if obj.payed_outline > 0:
        #        order.append({'name' : 'Предоплата:', 'value' : obj.payed_outline})



        #if hasattr(obj,'payed_by'):
        #    order.append({'name' : 'Оплачено на карту:', 'value' : obj.payed_outline})
        #if hasattr(obj,'payed_by'):
        #    if obj.payed_by != '':
        #        order.append({'name' : 'Оплачено от имени:', 'value' : obj.payed_by})

        return order

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            if not hasattr(obj,'credit'):
                return 0
            else:
                if obj.credit.status == 'signed':
                    return obj.price
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100

        if hasattr(obj,'credit'):
            if obj.credit.status == 'signed':
                total = total + obj.credit.items.summ*100

        return total/100

    def get_curator(self,obj):
        if obj.price != obj.payed_amount:
            return {}
        lis = []
        for x in obj.flow.pers_cur_toss.all():
            lis.append({'id': x.id,'title' : x.title})
        return {'price':obj.flow.pers_cur_price,'flow':obj.flow.id,'id':obj.id,'toss':lis}

    def get_cancelUrl(self, obj):
        return '/numer/api/schoolurl/'+str(obj.id)+'/'

    def get_buyCreditURL(self, obj):
        if self.get_amount(obj) == obj.price:
            return None
        return '/numer/api/schooltcburl/'+str(obj.id)+'/'

    def get_uploadDocumentUrl(self,obj):
        return '/numer/api/schoolupld/'+str(obj.id)+'/'

    def get_files(self,obj):
        files_array = []
        order = []

        for p in obj.files.all():
            files_array.append({'name':p.title,'value':reverse('file_download_school',kwargs={'pk':p.id}),'type':'url'})

        if len(files_array) > 0:
            order.append({'name':'Файлы','value':files_array,'type':'array'})
        else:
            order.append({'name':'Файлы','value':'Файлов нет','type':'caption'})

        return order[0]


    def get_prolong(self, obj):

        date_access = obj.flow.education_stop
        if hasattr(obj,'access_till') and obj.access_till is not None:
            date_access = obj.access_till

        date_access = '{}.{}.{}'.format(date_access.day,date_access.month, date_access.year)

        return {'price':obj.flow.extend_price,'access_date':date_access}

    def get_saleUrl(self, obj):

        if obj.price_f is not None:
            return None

        if obj.payed_amount == obj.price:
            return None

        return reverse('saleApply',kwargs={'id':obj.id})

    def get_flow_id(self, obj):
        return obj.flow.id

    def get_credit(self,obj):
        order = []
        status = ''
        if obj.credit.status == 'approved':
            status = 'Заявка одобрена'
        elif obj.credit.status == 'rejected':
            status = 'Отказ в выдаче кредита'
        elif obj.credit.status == 'canceled':
            status = 'Вы отменили заявку на кредит'
        elif obj.credit.status == 'signed':
            status = 'Кредитный договор подписан'

        order.append({'name' : 'Кредит для оплаты в системе №', 'value' : obj.credit.id, 'type' : 'id'})
        order.append({'name' : 'Сумма', 'value' : obj.credit.items.summ, 'type' : 'amount'})
        order.append({'name' : 'Статус', 'value' : status, 'type' : 'status'})
        order.append({'name' : 'Ссылка на анкету', 'value' : obj.credit.link_url, 'type' : 'link'})


        return order

    class Meta:
        model = SchoolAppForm
        fields = ['order','payment','amount','cform','curator','phone_valid','cancelUrl','uploadDocumentUrl','files','prolong','saleUrl','flow_id','buyCreditURL','credit']



class SchoolPersCuratorListSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(required=False, many = True)
    amount = serializers.SerializerMethodField(required=False)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100


    class Meta:
        model = SchoolAppPersCuratorForm
        fields = ['first_name','last_name','middle_name','email','phone','created','amount','payment','price']


class SchoolAppExtendFormListSerializer(serializers.ModelSerializer):

    payment = PaymentSerializer(required=False, many = True)
    amount = serializers.SerializerMethodField(required=False)
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount
        if obj.payed_amount > total/100:
            total = obj.payed_amount*100
        return total/100


    class Meta:
        model = SchoolExtendAccessService
        fields = ['first_name','last_name','middle_name','email','phone','created','amount','payment','price']


class SchoolCuratorListSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S",input_formats=['%d.%m.%Y'], required=False)


    class Meta:
        model = SchoolAppCurator
        fields = ['first_name','last_name','middle_name','email','phone','created','curator','expert']


class SchoolAppDiscountListSerializer(serializers.ModelSerializer):

    flow = serializers.SerializerMethodField(required=False)

    def get_flow(self, obj):
        flow_name = str(obj.flow.flow) +' '+ obj.flow.flow_name
        return flow_name

    class Meta:
        model = SchoolDiscount
        fields = '__all__'


class SchoolAppDiscountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDiscount
        fields = '__all__'


class SchoolExtendAccessServiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolExtendAccessService
        fields = ['form']

class SchoolExtendAccessServiceSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(required=False)

    payment = PaymentSerializer(required=False, many = True)

    amount = serializers.SerializerMethodField()

    cancelUrl = serializers.SerializerMethodField(required=False)

    def get_order(self,obj):
        order = []
        if not hasattr(obj,'id'):
            return order

        order.append({'name' : 'Заказ №', 'value' : obj.id, 'type' : 'id'})
        order.append({'name' : 'Поток обучения:', 'value' : obj.form.flow.flow, 'type' : 'flow_id'})
        order.append({'name' : 'Курс обучения:', 'value' : obj.form.flow.flow_name, 'type' : 'flow_name'})
        order.append({'name' : 'Анкета студента:', 'value' : obj.form.id, 'type' : 'form_id'})
 
        date_access = obj.form.flow.education_stop
        if hasattr(obj,'access_till') and obj.access_till is not None:
            date_access = obj.access_till

        date_access = '{}.{}.{}'.format(date_access.day,date_access.month, date_access.year)

        order.append({'name' : 'Доступ к материалам до:', 'value' : date_access, 'type' : 'date_access'})
        order.append({'name' : 'Фамилия:', 'value' : obj.form.last_name, 'type' : 'last_name'})
        order.append({'name' : 'Имя:', 'value' : obj.form.first_name, 'type' : 'first_name'})
        order.append({'name' : 'E-mail:', 'value' : obj.email, 'type' : 'email'})
        order.append({'name' : 'Телефон:', 'value' : obj.phone, 'type' : 'phone'})
        order.append({'name' : 'Стоимость услуги:', 'value' : obj.price, 'type' : 'price'})


        return order

    def get_amount(self,obj):
        total = 0
        if not hasattr(obj,'payment'):
            return 0
        for k in obj.payment.all():
            if k.is_paid():
                total += k.amount

        return total/100

    def get_cancelUrl(self, obj):
        return '/numer/api/schoolextendurl/'+str(obj.id)+'/'

    class Meta:
        model = SchoolExtendAccessService
        fields = ['order','payment','amount','cancelUrl','id']


class SchoolSaleFormSerializer(serializers.ModelSerializer):


    class Meta:
        model = SchoolExtendAccessService
        fields = ['order','payment','amount','cancelUrl','id']
