from app import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
# from .views import LoginView, LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('changePass', views.changePass, name='changePass'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('adminView', views.admin_view_time_logs, name='adminView'),
    path('pendingApplication', views.pendingApplication, name='pendingApplication'),
    path('approve_student/<int:id>/', views.approve_student, name='approve_student'),
    path('getAllPendingRegister', views.getAllPendingRegister, name='getAllPendingRegister'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
