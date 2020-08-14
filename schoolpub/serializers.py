from rest_framework import serializers
from .models import SchoolFAQPage
from .models import SchoolTextReviewsPage


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
        return obj.schooltextreviewspage.review.stream_data[0]['value']

    class Meta:
        model = SchoolTextReviewsPage
        fields = ['review']

