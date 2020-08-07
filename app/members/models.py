from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)


class MyList(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    place = models.ForeignKey(
        'tours.Place',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
