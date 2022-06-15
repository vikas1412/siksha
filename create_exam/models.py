from django.contrib.auth.models import User
from django.db import models


class QuestionOption(models.Model):
    question = models.ForeignKey("ExamQuestion", on_delete=models.CASCADE, null=True)
    option = models.CharField(max_length=500, null=True, blank=True)
    correctness = models.BooleanField(default=False)

    def __str__(self):
        return self.option


class ExamQuestion(models.Model):
    exam = models.ForeignKey("Exam", on_delete=models.SET_NULL, null=True)
    question = models.TextField(max_length=50000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.question


class Exam(models.Model):
    name = models.CharField(max_length=600, blank=None)
    batch = models.ManyToManyField("Batch", blank=True)
    date = models.DateField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    instructions = models.TextField(max_length=100000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    batch = models.CharField(max_length=2000, blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    users = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.batch


class ExamReport(models.Model):
    batch = models.ForeignKey("Batch", on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey("Exam", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    has_started = models.BooleanField(default=False)
    total_questions = models.IntegerField(blank=True, null=True)
    correct = models.IntegerField(blank=True, null=True)
    incorrect = models.IntegerField(blank=True, null=True)
    unattempted = models.IntegerField(blank=True, null=True)
    student_exam_duration_remaining = models.DurationField(null=True, blank=True)
    has_finished = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class UserResponse(models.Model):
    question = models.ForeignKey("ExamQuestion", on_delete=models.SET_NULL, null=True)
    selectedOption = models.ForeignKey("QuestionOption", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question


class UserInfo(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.email
