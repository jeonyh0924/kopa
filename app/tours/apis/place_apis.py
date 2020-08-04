from rest_framework.generics import ListAPIView, RetrieveAPIView

from tours.models import Place
from tours.serializers import PlaceSerializer, PlaceDetailSerializer


class PlaceAPIView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetailAPIView(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceDetailSerializer
