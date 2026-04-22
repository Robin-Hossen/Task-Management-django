from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def manager_dashboard(request):
    return render(request,"dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def task(request):
    context={
        'message':'This is the task page'
    }
    return render(request,'task.html',context)
