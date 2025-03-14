from django.shortcuts import render,HttpResponse



def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
    
def api_docs(request):
    return render(request, "api_docs.html")

def contact(request):
    return render(request, "contact.html")

def dashboardrepair(request):
    return render(request, "DashboardRepair.html")

def dashboardtechnician(request):
    return render(request, "DashboardTechnician.html")
    
def dashboardmanager(request):
    return render(request, "DashboardManager.html")

def faqs(request):
    return render(request, "FAQ.html")

def login(request):
    return render(request, "login.html")




