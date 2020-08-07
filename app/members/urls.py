from sys import path

from django.urls import include
from rest_framework import routers

from members.views import MyListAPIView

router = routers.SimpleRouter()
router.register('myList', MyListAPIView)
urlpatterns = router.urls
