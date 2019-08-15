from rest_framework import serializers
from .models import LikePost, LikeComment, LikeReply
from likes.serializers import LikesSerializer



class LikeCommentSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.request.user.is_anonymous:
            return False
        return obj.filter(id=self.request.user.id).exists()

    class Meta:
        model = LikeComment
        fields = ['cnt','liked']


class LikePostSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.request.user.is_anonymous:
            return False
        return obj.filter(id=self.request.user.id).exists()

    class Meta:
        model = LikePost
        fields = ['cnt','liked']



class LikeReplySerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.request.user.is_anonymous:
            return False
        return obj.filter(id=self.request.user.id).exists()

    class Meta:
        model = LikeReply
        fields = ['cnt','liked']


