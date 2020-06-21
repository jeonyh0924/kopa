from django.contrib import admin

# Register your models here.
from members.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username']


admin.site.register(User, UserAdmin)
