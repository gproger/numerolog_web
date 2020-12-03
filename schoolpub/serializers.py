from rest_framework import serializers
from .models import SchoolFAQPage
from .models import SchoolTextReviewsPage
from wagtail.images.models import Image

class SchoolFaqSerializer(serializers.ModelSerializer):

    faq = serializers.SerializerMethodField()

    def get_faq(self, obj):
        return obj.schoolfaqpage.faq.stream_data[0]['value']

    class Meta:
        model = SchoolFAQPage
        fields = ['faq']

class SchoolTextReviewsSerializer(serializers.ModelSerializer):

    review = serializers.SerializerMethodField()

    def get_review(self, obj):
        val = obj.schooltextreviewspage.review.stream_data[0]['value']
        for i in val:
            img = Image.objects.get(pk=i['image'])
            print(img)
            print(img.file)
            i['image'] = img.file.url
        return val

    class Meta:
        model = SchoolTextReviewsPage
        fields = ['review']

