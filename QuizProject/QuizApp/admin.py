from django.contrib import admin
from .models import Quiz, Question, Answer, UserResponse


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Quiz,QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text']


admin.site.register(Question,QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text']


admin.site.register(Answer,AnswerAdmin)


class UserResponseAdmin(admin.ModelAdmin):
    list_display = ['user','quiz','score','date_taken']


admin.site.register(UserResponse,UserResponseAdmin)