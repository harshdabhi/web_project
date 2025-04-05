from django.urls import path,re_path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("about",views.about,name='about'),
    path("login",views.login,name='login'),
    path("contact",views.contact,name='contact'),
    path("faqs",views.faqs,name='faqs'),
    path("assign",views.assign,name='assign'),
    path("logout",views.login,name='logout'),

    path("dashboardrepair",views.dashboardrepair,name='dashboardrepair'),
    path("dashboardtechnician",views.dashboardtechnician,name='dashboardtechnician'),
    path("dashboardmanager",views.dashboardmanager,name='dashboardmanager'),

    # Add path for machine/<int:machine_id> URL pattern
    path("machine/<int:machine_id>", views.machine_detail, name='machine_detail')


]
