from rest_framework import serializers
from .models import LikePost, LikeComment, LikeReply



class LikeCommentSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        print(self.context)
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikeComment
        fields = ['cnt','liked']


class LikePostSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        print(self.context)
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikePost
        fields = ['cnt','liked']



class LikeReplySerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        print(self.context)
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikeReply
        fields = ['cnt','liked']


