from django.contrib import admin
from AdminUser.models import User


class User_admin(admin.ModelAdmin):

    list_display = ['username']

admin.site.register(User,User_admin)

# Register your models here.
