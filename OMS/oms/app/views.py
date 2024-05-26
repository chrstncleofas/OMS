from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from app.models import CustomUser
from app.forms import EditProfileForm
from django.contrib import messages
from django.http import JsonResponse
from students.models import TableStudents, TimeLog
from django.core.mail import send_mail
from app.forms import CustomUserCreationForm
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

HOME_URL_PATH = 'app/base.html'
DASHBOARD = 'app/dashboard.html'
MAIN_DASHBOARD = 'app/main-dashboard.html'
PENDING_APPLICATION = 'app/pending.html'
PROFILE = 'app/profile.html'
CHANGE_PASSWORD = 'app/changePassword.html'

def home(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):        
    return render(request, HOME_URL_PATH)

def dashboard(request) -> HttpResponse:
    return render(request, DASHBOARD)

def mainDashboard(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    pending_students = TableStudents.objects.filter(is_approved=False)
    pending_count = pending_students.count()
    return render(
        request,
        MAIN_DASHBOARD,
        {
            'pending_count': pending_count,
            'firstName': firstName,
            'lastName': lastName
        }
    )

def profile(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=admin)
    return render(request, PROFILE, {
        'form': form,
        'firstName': firstName,
        'lastName': lastName
    })

def changePass(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name   
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePass')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, CHANGE_PASSWORD, {
        'form': form,
        'firstName': firstName,
        'lastName': lastName
    })

def getAllPendingRegister(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    students = TableStudents.objects.filter(is_approved=False)
    return render(request, PENDING_APPLICATION, {
        'getAllPendingRegister': students,
        'firstName': firstName,
        'lastName': lastName
    })

def pendingApplication(request) -> HttpResponse:
    return render(request, PENDING_APPLICATION)

def user_login(request) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'app/loginSuccess.html', {'message': 'Login successful!'})
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/base.html')

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

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_view_time_logs(request):
    students = TableStudents.objects.all()
    selected_student = None
    time_logs = None
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        selected_student = get_object_or_404(TableStudents, id=student_id)
        time_logs = TimeLog.objects.filter(student=selected_student).order_by('-timestamp')

    return render(
        request,
        'app/admin-test.html',
        {
            'students': students,
            'selected_student': selected_student,
            'time_logs': time_logs,
        }
    )