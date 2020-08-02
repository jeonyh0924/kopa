from django.urls import path
from rest_framework import routers

from tours.apis import ReviewAPIView
from tours.views import tourAPI

urlpatterns = [
    path('', tourAPI),
]

router = routers.SimpleRouter()
router.register('review', ReviewAPIView)

urlpatterns += router.urls
