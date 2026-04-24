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
        "person":
            {
                "name":"robin",
                "age":25,
                "villages":"kabli para",
                "city":"pabna"
            },
        
        "public":["horot","hafijul","asif","sabbir","jahid"],
        "list1":[1,2,3,4,5,6,7,8,9]

    }
    return render(request,'task.html',context)
