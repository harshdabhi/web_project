from django.urls import path,re_path
from . import views

urlpatterns=[
    path("",views.home,name='home'),
    path("about",views.about,name='about'),
    path("login/",views.login,name='login'),
    path("contact",views.contact,name='contact'),
    path("faqs",views.faqs,name='faqs'),

    path("dashboardrepair",views.dashboardrepair,name='dashboardrepair'),
    path("dashboardtechnician",views.dashboardtechnician,name='dashboardtechnician'),

]
