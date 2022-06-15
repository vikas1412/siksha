from django.contrib import admin
from create_exam.models import Exam, QuestionOption, ExamQuestion, UserResponse, Batch, ExamReport
from .models import UserInfo


@admin.register(ExamReport)
class ExamReportAdmin(admin.ModelAdmin):
    list_display = ('batch', 'exam', 'user', 'has_started', 'student_exam_duration_remaining', 'has_finished')


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'timestamp')
    inlines = [ExamQuestionInline]


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOption(admin.ModelAdmin):
    list_display = ('question', 'option')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('timestamp',)


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'password')


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selectedOption')
    ordering = ('user',)


# Display nested tables in admin
# from nested_inline.admin import NestedStackedInline, NestedModelAdmin
#
# class QuestionOptionInline(NestedStackedInline):
#     model = QuestionOption
#     extra = 0
#     fk_name = 'question'
#
#
# class ExamQuestionInline(NestedStackedInline):
#     model = ExamQuestion
#     extra = 1
#     fk_name = 'exam'
#     inlines = [QuestionOptionInline]
#
#
# class ExamAdmin(NestedModelAdmin):
#     model = Exam
#     list_display = ('name', 'duration', 'timestamp')
#     inlines = [ExamQuestionInline]
#
#
# admin.site.register(Exam, ExamAdmin)
