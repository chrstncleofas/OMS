from django.urls import reverse
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from students.forms import StudentRegistrationForm, UserForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

def studentHome(request) -> HttpResponse:
    return render(request, 'students/student-base.html')

def studentDashboard(request) -> HttpResponse:
    return render(request, 'students/student-dashboard.html')

def studentRegister(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.StudentID = student_form.cleaned_data['StudentID']
            student.Email = user.email
            student.Username = user.username
            student.Password = user.password
            student.save()     
            messages.success(request, 'Registration successful. Waiting for admin approval.')
            return render(request, 'students/success.html', {'message': 'Registration successful!'})
    else:
        user_form = UserForm()
        student_form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'user_form': user_form, 'student_form': student_form})

def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'students/loginSuccess.html', {'message': 'Login successful!'})
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')

def success(request):
    return render(request, 'students/success.html')

def loginSuccess(request):
    return render(request, 'students/loginSuccess.html')

def studentLogout(request) -> HttpResponseRedirect:
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect(reverse('students:home'))
