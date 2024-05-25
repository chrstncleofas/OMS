from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from students.models import TableStudents
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

HOME_URL_PATH = 'app/base.html'
DASHBOARD = 'app/dashboard.html'
MAIN_DASHBOARD = 'app/main-dashboard.html'

def home(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):        
    return render(request, HOME_URL_PATH)

def dashboard(request) -> HttpResponse:
    return render(request, DASHBOARD)

def mainDashboard(request):
    pending_students = TableStudents.objects.filter(is_approved=False)
    pending_count = pending_students.count()
    return render(
        request,
        MAIN_DASHBOARD,
        {'pending_count': pending_count}
    )

def getAllPendingRegister(request):
    students = TableStudents.objects.filter(is_approved=False)
    return render(request, MANAGE_STUDENT, {
        'getAllPendingRegister': students,
    })

def manageStudent(request) -> HttpResponse:
    return render(request, MANAGE_STUDENT)

def user_login(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(dashboard)
    return render(request, user_login)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, HOME_URL_PATH, {'form': form})

MANAGE_STUDENT = 'app/manage-student.html'
def approve_student(request, id):
    student = TableStudents.objects.get(id=id)
    student.is_approved = True
    student.save()
    messages.success(request, f'{student.Firstname} {student.Lastname} has been approved.')
    return redirect(reverse('manageStudent'))

def logoutView(request) -> HttpResponseRedirect:
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect(home)
