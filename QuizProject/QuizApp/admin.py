from django.contrib import admin
from .models import Quiz,Question,Answer,UserResponse


class UserResponse_admin(admin.ModelAdmin):
    list_display = ['user','quiz','score','date_taken']

admin.site.register(UserResponse,UserResponse_admin)


class Quiz_admin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Quiz,Quiz_admin)


class Question_admin(admin.ModelAdmin):
    list_display = ['question_text']
admin.site.register(Question,Question_admin)

class Answer_admin(admin.ModelAdmin):
    list_display = ['answer_text']
admin.site.register(Answer,Answer_admin)
