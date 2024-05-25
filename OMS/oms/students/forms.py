from django import forms
from students.models import StudentTable

class StudentRegistrationForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StudentTable
        fields = ['StudentID', 'Firstname', 'Lastname', 'Email', 'Course', 'Year', 'Username', 'Password']
