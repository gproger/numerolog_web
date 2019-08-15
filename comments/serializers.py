from rest_framework import serializers
from .models import CommentBlogThread, Comment, CommentReply
from likes.serializers import LikeCommentSerializer, LikeReplySerializer



class CommentReplySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    user = ShortUserSerializer()
    like = LikeReplySerializer(required=False)

    class Meta:
        model = Comment
        fields = ['text','date','user','like']



class CommentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)
    user = ShortUserSerializer()
    like = LikeCommentSerializer(required=False)
    reply = CommentReplySerializer(many=True, read_only = True, required=False)

    class Meta:
        model = Comment
        fields = ['text','date','user','like','reply']



class CommentBlogSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only = True)

    class Meta:
        model = CommentBlogThread
        fields = ['comment']
