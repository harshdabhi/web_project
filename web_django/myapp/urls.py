from django.urls import path,re_path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("about",views.about,name='about'),
    path("login",views.login,name='login'),
    path("contact",views.contact,name='contact'),
    path("faqs",views.faqs,name='faqs'),
    path("assign",views.assign,name='assign'),

    path("dashboardrepair",views.dashboardrepair,name='dashboardrepair'),
    path("dashboardtechnician",views.dashboardtechnician,name='dashboardtechnician'),
    path("dashboardmanager",views.dashboardmanager,name='dashboardmanager'),

    path("machine1",views.machine1,name='machine1'),
    path("machine2",views.machine2,name='machine2'),
    path("machine3",views.machine3,name='machine3'),
    path("machine4",views.machine4,name='machine4'),
    path("machine5",views.machine5,name='machine5'),
    path("machine6",views.machine6,name='machine6'),
]
