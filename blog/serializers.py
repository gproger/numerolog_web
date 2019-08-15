from rest_framework import serializers
from .models import PostPage
from wagtail.images.models import Image
from comments.serializers import CommentBlogSerializer
from likes.serializers import LikePostSerializer

class ImageWagtailCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields=['file']

class PostPageCustomSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes_serializer')
    header_image = ImageWagtailCustomSerializer(read_only=True, required=False)
    comments = serializers.SerializerMethodField('get_comments_serializer')
    last_published_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True,required=False)

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
        serializer = CommentBlogSerializer(obj.comments,read_only=True, context = serializer_context)
        return serializer.data

    class Meta:
        model = PostPage
        fields = ['id','title','body','comments','header_image','last_published_at','likes']
