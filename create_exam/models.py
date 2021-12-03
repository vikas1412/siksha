from django.contrib.auth.models import User
from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=600, blank=None)
    date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    instructions = models.TextField(max_length=100000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ExamQuestion(models.Model):
    exam = models.ForeignKey("Exam", on_delete=models.SET_NULL, null=True)
    question = models.TextField(max_length=50000, null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.question


class QuestionOption(models.Model):
    question = models.ForeignKey("ExamQuestion", on_delete=models.CASCADE, null=True)
    option = models.CharField(max_length=500, null=True, blank=True)
    correctness = models.BooleanField(default=False)

    def __str__(self):
        return f"ID for option:  {self.id}"


class UserResponse(models.Model):
    question = models.ForeignKey("ExamQuestion", on_delete=models.SET_NULL, null=True)
    selectedOption = models.ForeignKey("QuestionOption", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True)


class UserInfo(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.email


class ExamReport(models.Model):
    exam = models.ForeignKey("Exam", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    has_finished = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    student_exam_duration = models.DurationField(null=True, blank=True)
    total_questions = models.IntegerField()
    correct = models.IntegerField()
    incorrect = models.IntegerField()