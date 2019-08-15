from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CommentBlogThread, Comment, CommentReply
from likes.serializers import LikeCommentSerializer, LikeReplySerializer



class ShortUserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_user_name')

    def get_user_name(self,obj):
        r_name = obj.profile_fields.get('real_name')
        if len(r_name) > 0:
            return r_name
        else:
            return obj.username

    class Meta:
        model = get_user_model()
        fields = ['id','name']


class CommentReplySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    user = ShortUserSerializer()
    like = serializers.SerializerMethodField('get_like_serializer')


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
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    user = ShortUserSerializer()
    like = serializers.SerializerMethodField('get_like_serializer')
    reply = serializers.SerializerMethodField('get_reply_serializer')

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
        fields = ['text','date','user','like','reply','cnt']



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
