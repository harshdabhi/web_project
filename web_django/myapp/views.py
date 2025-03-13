from django.shortcuts import render,HttpResponse

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
    
def api_docs(request):
    return render(request, "api_docs.html")


