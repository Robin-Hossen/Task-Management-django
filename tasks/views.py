from django.contrib import messages

from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskDetailModelForm, TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from django.db.models import Q,Max,Min,Count,Avg#Q object ar kaj hosse complex query banano jemon amra jodi database theke task nia ashte chai jeta pending ache ba jeta due date 2026-04-23 tar age ache tahole amra Q object use kore ai query ta likhte parbo Task.objects.filter(Q(status="PENDING")|Q(due_date__lt="2026-04-23")) ai query te amra Q object use kore filter method er vitore complex query banate parbo 
                            #and amra Q object er vitore | operator use kore OR condition create korte parbo and & operator use kore AND condition create korte parbo and ~ operator use kore NOT condition create korte parbo.
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()#user ar group er vitore manager group ache kina check kore return kore true or false

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):


    type=request.GET.get("type",'all')#get method ar jonne type parameter nia aslam url theke jemon amra url a dile http://
    print(type)


    tasks=Task.objects.select_related("details").prefetch_related("assigned_to").all()#query kom korar select_related and prefetch_related use korechi.karon here is perform one to one and many to many relation.
    

    count=Task.objects.aggregate(
        total=Count('id'),
        completed_task=Count('id',filter=Q(status="COMPLETED")),
        in_progress_task=Count('id',filter=Q(status="IN_PROGRESS")),
        pending_tasks=Count('id',filter=Q(status="PENDING"))
        )
    

    #retriving task data
    base_query=Task.objects.select_related("details").prefetch_related("assigned_to")
    if type=="completed":
        tasks=base_query.filter(status="COMPLETED")
    elif type=="in_progress":
        tasks=base_query.filter(status="IN_PROGRESS")
    elif type=="pending":
        tasks=base_query.filter(status="PENDING")
    elif type=="total":
        tasks=base_query.all()    
    
    else: 
        tasks=base_query.all()           


    context={
        "tasks":tasks,
        "count":count
    }
    return render(request,"Dashboard/manager_dashboard.html",context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request,'Dashboard/user_dashboard.html')

def dashboard(request):
    return render(request,'Dashboard/dashboard.html')

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
@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    
    
    task_form=TaskModelForm()# for Get 
    task_detail_form=TaskDetailModelForm()# for Get

    #Post ar jonne
    if request.method=="POST":
        task_form=TaskModelForm(request.POST)# for Post
        task_detail_form=TaskDetailModelForm(request.POST)# for Post
        #print(form)
        if task_form.is_valid() and task_detail_form.is_valid():#valid check na korle data clean korte dei na
           task=task_form.save()#database a data entry ar jonne kaj hosse
           task_detail=task_detail_form.save(commit=False)#commit false ar mane hocche task_detail form er data save hobe na karon amra task_detail form er data te task ar data save korte chai tai commit false use korechi
           task_detail.task=task#task_detail form er task field te task_form er data save kortechi
           task_detail.save()#task_detail form er data save kortechi

           messages.success(request,"Task Added Successfully")#django te messages framework use kore amra user ke success message dekhate parbo jodi task successfully add hoy tahole amra user ke success message dekhate parbo and jodi task add na hoy tahole amra user ke error message dekhate parbo

           return redirect('create_task')

            
    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request,"task_form.html",context)


@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request,id):

    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task)# instance ar kaj hosse database theke specific task er data nia aslam and oi data dia form k populate kore dilam
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)# instance ar kaj hosse database theke specific task er details er data nia aslam and oi data dia form k populate kore dilam
    

    #Post ar jonne
    if request.method=="POST":
        task_form=TaskModelForm(request.POST,instance=task)# for Post
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)# for Post
        #print(form)
        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task updated Successfully")

            return redirect('update_task', id=task.id)

            
    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request,"task_form.html",context)


@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request,id):
    if request.method=="POST":
        task=Task.objects.get(id=id)
        task.delete()

        messages.success(request,"Task deleted successfully")
        return redirect('manager_dashboard')
    else:
        messages.error(request,"Invalid request method")
        return redirect('manager_dashboard')




#here i learn queryset filter and exclude and other querysets..(queryset.com) a gele onek gulo querysets er option dekhte parbo and ai gulo diye amra database theke specific data nia ashte parbo
 
#def view_tasks(request):
    #tasks=Task.objects.all()#database theke sob task nia aslam
    # context={
    #     "tasks":tasks
    # }
    # #retrive specific task
    # return render(request,"show_task.html",context)

    #task =Task.objects.filter(status="PENDING")#filter ar kaj hosse database theke specific data nia aslam 
    #task=TaskDetail.objects.exclude(priority="H")#exclude ar kaj hosse database theke specific data bad dia nia aslam
    #return render(request,"show_task.html",{"task":task})



#select_related and prefetch_related (foreign and ono to one key ar jonne select_related and many to many ar jonne prefetch_related use kora hoy)
#def view_tasks(request):
    # task=Task.objects.select_related("details").all()#select_related ar kaj hosse foreign key ar jonne database theke data nia aslam and details ar data o nia aslam karon amra select_related use korechi and details ar data task er details ar vitore thake tai amra task er details ar vitore details ar data nia aslam
    #task=TaskDetail.objects.select_related("task").all()#select_related ar kaj hosse foreign key ar jonne database theke data nia aslam and task ar data o nia aslam karon amra select_related use korechi and task ar data taskdetail ar vitore thake tai amra taskdetail er task ar vitore task ar data nia aslam
    #task=Task.objects.select_related("project").all()#select_related ar kaj hosse foreign key ar jonne database theke data nia aslam and project ar data o nia aslam karon amra select_related use korechi and project ar data task er project ar vitore thake tai amra task er project ar vitore project ar data nia aslam
   # task=Project.objects.prefetch_related("task_set").all()#prefetch_related ar kaj hosse many to many and reverse_relation key ar jonne kaj kore and task ar data o nia aslam karon amra prefetch_related use korechi and task ar data project er vitore thake tai amra project er task_set ar vitore task ar data nia aslam
    #task_set hosse default related name jeta django provide kore many to many ar jonne and task_set ar vitore task ar data thake karon amra prefetch_related use korechi 

   # return render(request,"show_task.html",{"task":task})



#use aggregate function to calculate max, min, count and average of a field in a queryset
@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_tasks(request):  
    # task_count=Task.objects.aggregate(num_count=Count('id'))#count ar kaj hosse database theke task er total count nia aslam
    
    projects=Project.objects.annotate(task_count=Count('task')).order_by('task_count')#annotate ar kaj hosse database theke project er sathe task er count nia aslam karon amra annotate use korechi and task_set ar vitore task er data thake karon amra prefetch_related use korechi and task_set ar vitore task er data thake tai amra project er sathe task er count nia aslam
    return render(request,"show_task.html",{"projects":projects})


@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def task_details(request,task_id):
    task=Task.objects.get(id=task_id)
    return render(request,"task_details.html",{"task":task})



