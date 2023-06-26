from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('lab/signup/', views.LabUserSignupView.as_view(), name="signup"),
    path('lab/login/', views.LabUserLoginView.as_view(), name='lablogin'),
    path('lab/test/add/', views.TestAddView.as_view(), name="testAdd"),
    path('lab/test/', views.TestListView.as_view(), name="testList"),
    path('lab/test/update/<str:test_id>/', views.TestUpdateView.as_view(), name="testUpdate"),
    path('lab/test/delete/<str:test_id>/', views.TestDeleteView.as_view()),
    path('lab/register/', views.AssignTestViewTemp.as_view(), name="labregister"),
    path('lab/register/print/<str:visit_id>/', views.LabRegisterPrint.as_view(), name="labregisterprint"),
    path('patient/login/', views.PatientLoginView.as_view(), name="patientlogin"),
    path('patient/home/', views.PatientHome.as_view(), name="patienthome"),
    path('patient/logout/', views.PatientLogout.as_view(), name="patientlogout"),
    path('patient/tests/<str:id>/', views.PatientTestsView.as_view(), name="patienttests"),
    path('lab/home/', views.LabUserHome.as_view(), name="labhome"),
    path('lab/logout', views.LabLogout.as_view(), name="lablogout"),
]
