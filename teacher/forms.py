from django import forms
from django.contrib.auth.models import User
from teacher.models import Teacher

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['user']  # Ya lo estás asignando por código, así que no lo edites aquí
