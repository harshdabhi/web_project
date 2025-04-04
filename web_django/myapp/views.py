from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

    
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
    
def api_docs(request):
    return render(request, "api_docs.html")

def contact(request):
    return render(request, "contact.html")

def dashboardrepair(request):
    return render(request, "dashboardRepair.html")

def dashboardtechnician(request):
    return render(request, "dashboardTechnician.html")
    
def dashboardmanager(request):
    return render(request, "dashboardManager.html")

def faqs(request):
    return render(request, "FAQ.html")

def machine1(request):
    return render(request, "machine1.html")

def machine2(request):
    return render(request, "machine2.html")

def machine3(request):
    return render(request, "machine3.html")

def machine4(request):
    return render(request, "machine4.html")

def machine5(request):
    return render(request, "machine5.html")

def machine6(request):
    return render(request, "machine6.html")
    

def user_logout(request):
    logout(request)
    return redirect('home.html')

def assign(request):
    return render(request, "assign.html")




