from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)


class MyList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    mylist = models.ForeignKey('MyList', on_delete=models.CASCADE, blank=True, null=True,help_text='나의 즐겨찾는 관광지 리스트')
