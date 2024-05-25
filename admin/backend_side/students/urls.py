from students import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'students'

urlpatterns = [
    path('', views.studentHome, name='studentHome'),
    path('login', views.studentLogin, name='login'),
    path('studentRegister/', views.studentRegister, name='studentRegister'),
    path('studentDashboard/', views.studentDashboard, name='studentDashboard'),
    path('logout/', views.studentLogout, name='logout'),
    path('success/', views.success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
