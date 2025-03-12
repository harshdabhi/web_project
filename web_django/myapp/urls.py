from django.urls import path
from . import views

# Just add pages routes here 

urlpatterns=[
    # path to home page
    path("",views.home,name='home'),

    # path to about us page
    path("about",views.about,name='about'),

    
]