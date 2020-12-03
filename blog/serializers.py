from rest_framework import serializers
from .models import PostPage
from .models import ServicePage
from .models import SchoolPublicPage
from taggit.models import Tag
from .models import TermsOfServicePage
from wagtail.images.models import Image
from comments.serializers import CommentShortBlogSerializer
from likes.serializers import LikePostSerializer
from favorites.serializers import FavoritesPostSerializer

import datetime
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta


class ImageWagtailCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields=['file']

class PostPageCustomSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes_serializer')
    header_image = ImageWagtailCustomSerializer(read_only=True, required=False)
    comments = serializers.SerializerMethodField('get_comments_serializer')
#    last_published_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    tags = serializers.SerializerMethodField('get_tags_serializer')
    last_published_at = serializers.SerializerMethodField('get_published_date')
    fav = serializers.SerializerMethodField('get_favorite_serializer')
    date = serializers.SerializerMethodField('get_date_spec')
    tz = tzutc()
    url = serializers.SerializerMethodField('get_url_front')

    def get_date_spec(self, obj):
        return obj.last_published_at

    def get_url_front(self,obj):
        return '/blog/view/'+str(obj.id)+'/'

    def get_published_date(self,obj):
        d_now = datetime.datetime.now(tz=self.tz)
        d_rel = relativedelta(dt1=d_now,dt2=obj.last_published_at)
        if d_rel.years > 0:
            return str(d_rel.years) + ' г.'
        if d_rel.months > 0:
            return str(d_rel.months) + ' мес.'
        if d_rel.weeks > 0:
            return str(d_rel.weeks) + ' нед.'
        if d_rel.days > 0:
            return str(d_rel.days) + ' д.'
        if d_rel.hours > 0:
            return str(d_rel.hours) + ' ч.'
        if d_rel.minutes > 0:
            return str(d_rel.minutes) + ' мин.'
        if d_rel.seconds > 0:
            return str(d_rel.seconds) + ' сек.'

    def get_tags_serializer(self, obj):
        if not hasattr(obj,'tags'):
            return None

        return obj.tags.names()

    def get_likes_serializer(self, obj):
        if not hasattr(obj,'likes'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = LikePostSerializer(obj.likes,read_only=True, context = serializer_context)
        return serializer.data

    def get_favorite_serializer(self, obj):
        if not hasattr(obj,'favs'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = FavoritesPostSerializer(obj.favs,read_only=True, context = serializer_context)
        return serializer.data

    def get_comments_serializer(self, obj):
        if not hasattr(obj,'comments'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = CommentShortBlogSerializer(obj.comments,read_only=True, context = serializer_context)
        return serializer.data

    class Meta:
        model = PostPage
        fields = ['id','title','body','comments','header_image','last_published_at','likes','tags','fav','date','url']

class TermsOfServiceCustomShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsOfServicePage
        fields = ['id','title']



class ServiceAboutStreamDataSerializer(serializers.Serializer):

#    image=ImageWagtailCustomSerializer(source=get_image,read_only=True)
    desc = serializers.CharField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return Image.objects.get(id=obj['image']).file.url

class ServicesCustomSerializer(serializers.ModelSerializer):
    toss = TermsOfServiceCustomShortSerializer(many=True, read_only=True)
    order = serializers.SerializerMethodField(read_only=True)
    image_light = ImageWagtailCustomSerializer(read_only=True)
    image_dark = ImageWagtailCustomSerializer(read_only=True)
    about = serializers.SerializerMethodField()

    def get_order(self, obj):
        return {
            'kids_cnt' : obj.kids_cnt,
            'adult_cnt' : obj.adult_cnt,
            'comp_parent' : obj.comp_parent,
            'impr_chld' : obj.impr_chld,
            'price' : obj.price,
        }

    def get_about(self, obj):
        if obj.about.stream_data:
            if 'value' in obj.about.stream_data[0]:
                return ServiceAboutStreamDataSerializer(obj.about.stream_data[0]['value'], many=True).data
            else:
                return []
        else:
            return []

    class Meta:
        model = ServicePage
        fields = ['price','expert','date_cnt','date','title','toss','id','order','image_light','image_dark','about','whatInclude','bgColor','textColor','order_num']

class TermsOfServiceCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsOfServicePage
        fields = ['id','descr','date','title']


class SchoolPublicCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolPublicPage
        fields = ['id','html','date','title']
