from rest_framework import serializers
from .models import PostPage
from .models import ServicePage
from wagtail.images.models import Image
from comments.serializers import CommentShortBlogSerializer
from likes.serializers import LikePostSerializer
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
    last_published_at = serializers.SerializerMethodField('get_published_date')
    tz = tzutc()
    d_now = datetime.datetime.now(tz=tz)

    def get_published_date(self,obj):
        d_rel = relativedelta(dt1=self.d_now,dt2=obj.last_published_at)
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


    def get_likes_serializer(self, obj):
        if not hasattr(obj,'likes'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = LikePostSerializer(obj.likes,read_only=True, context = serializer_context)
        return serializer.data

    def get_comments_serializer(self, obj):
        if not hasattr(obj,'comments'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = CommentShortBlogSerializer(obj.comments,read_only=True, context = serializer_context)
        return serializer.data

    class Meta:
        model = PostPage
        fields = ['id','title','body','comments','header_image','last_published_at','likes']


class ServicesCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServicePage
        fields = ['descr','price','expert','date_cnt','date','title']
