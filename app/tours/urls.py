from django.urls import path

from tours.views import tourAPI

urlpatterns = [
    path('', tourAPI),
]