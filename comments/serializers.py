from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CommentBlogThread, Comment, CommentReply
from likes.serializers import LikeCommentSerializer, LikeReplySerializer
import datetime
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta


class ShortUserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_user_name')
    avatar = serializers.SerializerMethodField('get_avatar_serializer')

    def get_user_name(self,obj):
        r_name = obj.profile_fields.get('real_name')
        if len(r_name) > 0:
            return r_name
        else:
            return obj.username

    def get_avatar_serializer(self,obj):
        for i in obj.avatars:
            if i.get('size') == 64:
                return i.get('url')

    class Meta:
        model = get_user_model()
        fields = ['id','name','avatar']


class CommentReplySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('get_diff_time')
    user = ShortUserSerializer()
    like = serializers.SerializerMethodField('get_like_serializer')
    tz = tzutc()
    d_now = datetime.datetime.now(tz=tz)

    def get_diff_time(self,obj):
        d_rel = relativedelta(dt1=self.d_now,dt2=obj.date)
        print(d_rel)
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

    def get_like_serializer(self, obj):
        if not hasattr(obj,'like'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = LikeReplySerializer(obj.like,read_only=True, context = serializer_context)
        return serializer.data


    class Meta:
        model = Comment
        fields = ['text','date','user','like']



class CommentSerializer(serializers.ModelSerializer):
    #date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    date = serializers.SerializerMethodField('get_diff_time')
    user = ShortUserSerializer()
    like = serializers.SerializerMethodField('get_like_serializer')
    reply = serializers.SerializerMethodField('get_reply_serializer')
    tz = tzutc()
    d_now = datetime.datetime.now(tz=tz)

    def get_diff_time(self,obj):
        d_rel = relativedelta(dt1=self.d_now,dt2=obj.date)
        print(d_rel)
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





    def get_like_serializer(self, obj):
        if not hasattr(obj,'like'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = LikeCommentSerializer(obj.like,read_only=True, context = serializer_context)
        return serializer.data

    def get_reply_serializer(self, obj):
        if not hasattr(obj,'reply'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = CommentReplySerializer(obj.reply,read_only=True, context = serializer_context, many=True, required=False)
        return serializer.data


    class Meta:
        model = Comment
        fields = ['id','text','date','user','like','reply','cnt']



class CommentBlogSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField('get_comment_serializer')

    def get_comment_serializer(self, obj):
        if not hasattr(obj,'comment'):
            return None
        serializer_context = {'request':self.context.get('request')}
        serializer = CommentSerializer(obj.comment,read_only=True, context = serializer_context, many = True)
        return serializer.data


    class Meta:
        model = CommentBlogThread
        fields = ['id','comment','cnt']


class CommentShortBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentBlogThread
        fields = ['id','cnt']