from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from members.models import MyList
from members.permissions import MyListIsOwnerOrReadOnly
from members.serializers import MyListSerializers


class MyListAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = MyList.objects.all()
    serializer_class = MyListSerializers

    def get_permissions(self):
        if self.action == 'destroy':
            return (MyListIsOwnerOrReadOnly(),)
        return (AllowAny(), )

    def get_queryset(self):
        if self.request.user.pk is not None:
            qs = super().get_queryset().filter(user=self.request.user)
        else:
            qs = []
        return qs
