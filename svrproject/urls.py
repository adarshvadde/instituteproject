"""svrproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from svr import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentsignup/', views.student_signup_view, name='studentsignup'),
    path('studentlogin/', views.student_login_view, name='studentlogin'),
    path('forgetpassword/', views.forget_password_view, name='forgetpassword'),
    path('applicationform/<studentid>',views.application_view,name='applicationform'),
    path('application_view_data/<value>',views.application_view_data,name='application_view_data'),
    path('applications/', views.application_list_view, name='application-list'),
    path('emailsender/',views.emailsender,name='emailsender'),
    path('sendemails/',views.sendemails,name='sendemails'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_transposed/', views.attendance_transposed, name='attendance_transposed'),
    path('', views.student_home_view, name='studenthome'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('forget_send_otp/', views.forget_send_otp, name='forget_send_otp'),
    path('forget_verify_otp/', views.forget_verify_otp, name='forget_verify_otp'),
    path('applicatinsform/<studentid>',views.applicatinsform,name="applicatinsform"),
    path('extend2/',views.extendshtml2,name="extend2"),
    path('extend3/',views.extendshtml3,name="extend3"),
    path('adminpage/<adminid>',views.adminpage,name='adminpage'),
    path('adminpagestudentlist/<adminid>',views.adminpagestudentlist,name='adminpagestudentlist'),
    path('adminstudentprofile/<adminid>/<studentid>',views.adminstudentprofile,name="adminstudentprofile"),
    path('adminstudentdailyatendance/<adminid>',views.adminstudentdailyatendance,name="adminstudentdailyatendance"),
    path('adminapplicationformslist/<adminid>',views.adminapplicationformslist, name='adminapplicationformslist'),
    path('adminapplicationformsstudent/<adminid>/<studentuniqueid>',views.adminapplicationformsstudent, name='adminapplicationformsstudent'),
    path('adminpagetakeingattendance/<adminid>',views.adminpagetakeingattendance,name='adminpagetakeingattendance'),
    path('adminemailsender/<adminid>',views.adminemailsender,name="adminemailsender"),
    path('api/search_suggestions/', views.search_suggestions_api, name='search_suggestions_api'),
    path('details/<adminid>/<str:student_id>/', views.application_detail, name='application_detail'),
    path('studentprofile/<studentuniqueid>',views.studentprofile,name='studentprofile'),
    path('studenthome/<studentuniqueid>',views.studenthome,name='studenthome'),
    path('studentapplications/<studentuniqueid>',views.studentapplications,name="studentapplications"),
    path('studentapplicationform/<studentuniqueid>',views.studentapplicationform,name="studentapplicationform"),
    path('studentattendance/<studentuniqueid>',views.studentattendance,name="studentattendance"),
    path('studentemailconform/<studentid>',views.studentemailconform,name="studentemailconform"),
    path('studentweeklyreport/<studentid>',views.studentweeklyreport,name="studentweeklyreport"),
    path('studentaddweeklyreport/<studentid>/<fromto>',views.studentaddweeklyreport,name="studentaddweeklyreport"),
    path('studentweeklyreports/<studentid>',views.studentweeklyreports,name="studentweeklyreports"),




]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

