from django import forms
from .models import UserInfo, Exam, Batch


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['fullname', 'email', 'password']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'id': 'fullname'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'id': 'password'}),
        }


class NewExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'duration', 'instructions']
        error_messages = {"required": "This field is required."}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-12', 'id': 'name'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control col-md-6', 'type': 'date', 'id': 'date'}),
            # 'duration': forms.TimeInput(attrs={'class': 'form-control col-md-6', 'id': 'duration'}),
            'instructions': forms.TextInput(attrs={'class': 'form-control col-12 vLargeTextField', 'id': 'instructions'}),

        }


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch', 'status', 'users',]
