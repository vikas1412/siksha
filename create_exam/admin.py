from django.contrib import admin
from create_exam.models import Exam, QuestionOption, ExamQuestion, UserResponse, Todo

admin.site.register((Exam, ExamQuestion, QuestionOption, UserResponse, Todo))
