from django import forms
from .models import UserInfo


class StudentRegistration(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['fullname', 'email', 'password']
        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control', 'id':'fullname'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'id':'email'}),
            'password': forms.TextInput(attrs={'class':'form-control', 'id':'password'}),
        }
