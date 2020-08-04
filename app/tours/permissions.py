from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    credit : 이란 변수 안에, 비 로그인 유저의 패스워드를 넣고 수정 요청 시 확인을 한다.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.password == request.data['credit']
