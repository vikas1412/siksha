from django.contrib import admin
from create_exam.models import Exam, QuestionOption, ExamQuestion, UserResponse
from .models import UserInfo

admin.site.register((Exam, ExamQuestion, QuestionOption, UserResponse))


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'password')
