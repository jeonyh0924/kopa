from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tours.models import ReviewComment
from tours.permissions import IsOwnerOrReadOnly
from tours.serializers import ReviewCommentSerializer


class ReviewAPIView(ModelViewSet):
    """
    댓글은 비 로그인 유저가 생성 시에는 password가 입력 되어야 하고, 로그인 유저는 username의 20자 까지 된다.

    수정과 삭제 시 request에는 credit이라는 변수 안에 댓글에 대한 password가 작성이 되어야 한다.
    - 비 로그인 유저는 직접 입력
    - 로그인 된 유저는 유저네임으로
    # 위 동작을 모델 코드 안에 넣어야 할 것 같습니다.
    """
    queryset = ReviewComment.objects.all()
    serializer_class = ReviewCommentSerializer

    def create(self, request, *args, **kwargs):
        if request.user.pk is not None:
            request.data._mutable = True
            if len(request.user.username) > 20:
                request.data['password'] = request.user.username[:20]
            else:
                request.data['password'] = request.user.username
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()
