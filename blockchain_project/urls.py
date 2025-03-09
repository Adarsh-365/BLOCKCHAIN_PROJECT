"""
URL configuration for blockchain_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('user_reg',views.user_registration,name='user_reg'),
    path('forget_pass',views.forget_pass,name='forget_pass'),
    path('official_reg',views.officail_registration,name='official_reg'),
    path('main',views.main,name='main'),
    path('tab',views.tab,name='tab'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('clerkdashboard/', views.clerk_dashboard, name='clerkdashboard'),
    path('district-collector-dashboard/', views.district_collector_dashboard, name='districtcollectordashboard'),
    path('joint-collector-dashboard/', views.joint_collector_dashboard, name='jointcollectordashboard'),
    path('ministry-welfare-dashboard/', views.ministry_welfare_dashboard, name='ministryofwelfaredashboard'),
    path('mro-dashboard/', views.mro_dashboard, name='mrodashboard'),
    path('project-officer-dashboard/', views.project_officer_dashboard, name='projectofficerdashboard'),
    path('revenue-department-dashboard/', views.revenue_department_dashboard, name='revenuedepartmentofficerdashboard'),
    path('revenue-inspector-dashboard/', views.revenue_inspector_dashboard, name='revenueinspectordashboard'),
    path('superintendent-dashboard/', views.superintendent_dashboard, name='superintendentdashboard'),
    path('surveyor-dashboard/', views.surveyor_dashboard, name='surveyordashboard'),
    path('ministry_of_welfare_dashboard/', views.ministry_of_welfare_dashboard, name='ministryofwelfaredashboard'),
    
    path('load_tab/<int:tab>/', views.load_tab, name='load_tab'),
    
    
]
