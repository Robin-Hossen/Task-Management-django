from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

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


#before create django model form


# def create_task(request):
#     #database theke employy der nia aslm then taskForm k call dlm oi data dia
#     employees=Employee.objects.all()
#     form=TaskForm(employees=employees)# for Get 

#     #Post ar jonne
#     if request.method=="POST":
#         form= TaskForm(request.POST,employees=employees)
#         #print(form)
#         if form.is_valid():#valid check na korle data clean korte dei na
#             #why clean , karon data ar sate onek html format dei ai jonne ata default
#             #print(form.cleaned_data)
#             data=form.cleaned_data #data base a data entry ar jonne kaj hosse
#             title=data.get('title')
#             description=data.get('description')
#             due_date=data.get('due_date')
#             assigned_to=data.get('assigned_to')

#             task=Task.objects.create(title=title,description=description,due_date=due_date)


#             #Assign employee to tasks
#             for emp_id in assigned_to:
#                 employee=Employee.objects.get(id=emp_id)
#                 task.assigned_to.add(employee)

#             return HttpResponse("Task Added Successfully")   

#     context={
#         "form":form
#     }
#     return render(request,"task_form.html",context)





#after create a django model form

def create_task(request):
    
    
    form=TaskModelForm()# for Get 

    #Post ar jonne
    if request.method=="POST":
        form= TaskModelForm(request.POST)
        #print(form)
        if form.is_valid():#valid check na korle data clean korte dei na
            form.save()

            return render(request,'task_form.html',{"form":form,"message":"task added successfully"})

            
    context={
        "form":form
    }
    return render(request,"task_form.html",context)
