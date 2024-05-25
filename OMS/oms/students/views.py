from django.urls import reverse
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from students.forms import StudentRegistrationForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

def studentHome(request) -> HttpResponse:
    return render(request, 'students/student-base.html')

def studentDashboard(request) -> HttpResponse:
    return render(request, 'students/student-dashboard.html')

def studentRegister(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Waiting for admin approval.')
            return redirect('students:studentHome')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/student-base.html', {'form': form})

def studentLogin(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('students:studentDashboard')
        else:
            messages.error(request, 'Your account is disabled.')
    return render(request, 'students/login.html')

def success(request):
    return render(request, 'students/success.html')

def studentLogout(request) -> HttpResponseRedirect:
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect(reverse('students:studentHome'))  # Gumamit ng reverse function para sa pangalan ng ruta
