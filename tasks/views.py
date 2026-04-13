from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, <h2>welcome to the Django Project!</h2>")
def contact(request):
    return HttpResponse("This is mera contact page ")

def show_task(request):
    return HttpResponse("show task page")

    
