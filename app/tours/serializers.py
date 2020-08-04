from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tours.models import ReviewComment, Place


class ReviewCommentSerializer(ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'title', 'content', 'password')


class PlaceSerializer(ModelSerializer):
    # tags = serializers.StringRelatedField(many=True, source='tags.all')

    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'content',
            'address',
            'average_score',
            'phone_number',
            'open_time',
            'url',
            'trans',
            'release_date',
            'tags'
        )


class PlaceDetailSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = (
            '__all__',
        )
