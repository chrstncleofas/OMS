from django import forms
from app.models import CustomUser
from students.models import TableStudents

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class StudentRegistrationForm(forms.ModelForm):
    StudentID = forms.CharField(max_length=10, label='Student ID')

    class Meta:
        model = TableStudents
        fields = ['StudentID', 'Firstname', 'Lastname', 'Course', 'Year']
