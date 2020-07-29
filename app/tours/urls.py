from django.urls import path

from tours.views import tourAPI, otherRequsetAPI

urlpatterns = [
    path('', tourAPI),
    path('other/', otherRequsetAPI),
]