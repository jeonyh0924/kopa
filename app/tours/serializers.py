from rest_framework.serializers import ModelSerializer

from tours.models import ReviewComment


class ReviewCommentSerializer(ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'title', 'content', 'password')
