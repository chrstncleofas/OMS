from app import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
# from .views import LoginView, LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('manageStudent', views.manageStudent, name='manageStudent'),
    path('getAllPendingRegister', views.getAllPendingRegister, name='getAllPendingRegister'),
    path('approve_student/<int:id>/', views.approve_student, name='approve_student'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
