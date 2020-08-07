from rest_framework.serializers import ModelSerializer

from members.models import MyList


class MyListSerializers(ModelSerializer):
    """
    유저가 누군지에 대한 정보는 넣지 않았습니다.
    플레이스는 전체 데이터가 아닌 축약된
    ListPlaceSerializer가 생기게 된다면 해당 시리얼라이저를 넣어
    리스트 안에 넣는게 어떨까 라는 아이디어가 있습니다.
    """
    class Meta:
        model = MyList
        fields = (
            'id', 'user', 'place',
        )
        extra_kwargs = {
            'user': {'write_only': True},
        }
