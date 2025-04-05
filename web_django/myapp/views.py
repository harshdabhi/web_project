from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

    
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
    
def login(request):
    return render(request,"login.html")
    
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

def machine_detail(request, machine_id):
    # This view will handle the machine detail page
    # You can fetch machine details from the database using the machine_id
    # For now, we will just render a template with the machine_id
    return render(request, "machine.html", {"machine_id": machine_id})
    

def user_logout(request):
    logout(request)
    return redirect('home.html')

def assign(request):
    return render(request, "assign.html")




