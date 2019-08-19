from rest_framework import serializers
from .models import LikePost, LikeComment, LikeReply
from comments.models import CommentReply, Comment


class LikePostSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikePost
        fields = ['cnt','liked']


class LikeCommentSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikeComment
        fields = ['cnt','liked']


class LikeReplySerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self,obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return obj.likes.filter(id=self.context.get('request').user.id).exists()

    class Meta:
        model = LikeReply
        fields = ['cnt','liked']


class LikePostAddSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        postPage = self.context.get('postPage',None)
        likes = None
        user = self.context.get('request',None).user
        if hasattr(postPage,'likes'):
            likes = postPage.likes
        else:
            likes = LikePost.objects.create(post=postPage)
        if likes.likes.filter(pk=user.pk).count() == 0:
            likes.cnt = likes.cnt + 1
        likes.likes.add(user)

        likes.save()
        return likes

    class Meta:
        model = LikePost
        fields = ['cnt']


class LikeCommentAddSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        comment_id = self.context.get('id')
        comment = Comment.objects.get(pk=comment_id)
        likes = None
        user = self.context.get('request',None).user
        if hasattr(comment,'likes'):
            likes = comment.likes
        else:
            likes = LikeComment.objects.create(comment=comment)
        if likes.likes.filter(pk=user.pk).count() == 0:
            likes.cnt = likes.cnt + 1
        likes.likes.add(user)

        likes.save()
        return likes

    class Meta:
        model = LikeComment
        fields = ['cnt']


class LikeReplyAddSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        reply_id = self.context.get('id')
        commentReply = CommentReply.objects.get(pk=reply_id)
        likes = None
        user = self.context.get('request',None).user
        if hasattr(commentReply,'likes'):
            likes = commentReply.likes
        else:
            likes = LikeReply.objects.create(reply=commentReply)
        if likes.likes.filter(pk=user.pk).count() == 0:
            likes.cnt = likes.cnt + 1
        likes.likes.add(user)

        likes.save()
        return likes

    class Meta:
        model = LikeReply
        fields = ['cnt']
