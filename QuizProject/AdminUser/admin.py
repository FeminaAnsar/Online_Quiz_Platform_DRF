from django.contrib import admin
from AdminUser.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ['username']

admin.site.register(User,UserAdmin)

# Register your models here.
