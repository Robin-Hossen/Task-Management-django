from django.contrib import messages

from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskDetailModelForm, TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from django.db.models import Q,Max,Min,Count,Avg#Q object ar kaj hosse complex query banano jemon amra jodi database theke task nia ashte chai jeta pending ache ba jeta due date 2026-04-23 tar age ache tahole amra Q object use kore ai query ta likhte parbo Task.objects.filter(Q(status="PENDING")|Q(due_date__lt="2026-04-23")) ai query te amra Q object use kore filter method er vitore complex query banate parbo 
                            #and amra Q object er vitore | operator use kore OR condition create korte parbo and & operator use kore AND condition create korte parbo and ~ operator use kore NOT condition create korte parbo.
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView
from django.views.generic import DetailView,UpdateView







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




#after create a django model form
@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    
    
    task_form=TaskModelForm()# for Get 
    task_detail_form=TaskDetailModelForm()

    #Post ar jonne
    if request.method=="POST":
        task_form=TaskModelForm(request.POST)# for Post
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)# for Post
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


#create Task replace by class view
#variables for list of decorators
create_task_decorators=[login_required,permission_required('tasks.add_task', login_url='no-permission')]
# @method_decorator(create_task_decorators, name='dispatch')#method_decorator ar kaj hosse class based view er method gulo te decorator apply kora jemon amra jodi class based view er get method ar vitore login_required and permission_required decorator apply korte chai tahole amra method_decorator use korechi and dispatch method ar vitore login_required and permission_required decorator apply korechi karon dispatch method ar vitore get, post, put, delete method gulo call hoy tai amra dispatch method ar vitore login_required and permission_required decorator apply korechi tahole get, post, put, delete method gulo te login_required and permission_required decorator apply hoye jabe

class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):

    permission_required='tasks.add_task'
    login_url='sign-in'
    template_name="task_form.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["task_form"]=kwargs.get("task_form",TaskModelForm())
        context["task_detail_form"]=kwargs.get("task_detail_form",TaskDetailModelForm())
        return context
    
    def get(self,request,*args,**kwargs):
        
        context=self.get_context_data()
        return render(request,self.template_name,context)
    

    def post(self,request,*args,**kwargs):
        task_form=TaskModelForm(request.POST)# for Post
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)# for Post
        #print(form)
        if task_form.is_valid() and task_detail_form.is_valid():#valid check na korle data clean korte dei na
           task=task_form.save()#database a data entry ar jonne kaj hosse
           task_detail=task_detail_form.save(commit=False)#commit false ar mane hocche task_detail form er data save hobe na karon amra task_detail form er data te task ar data save korte chai tai commit false use korechi
           task_detail.task=task#task_detail form er task field te task_form er data save kortechi
           task_detail.save()#task_detail form er data save kortechi

           messages.success(request,"Task Added Successfully")#django te messages framework use kore amra user ke success message dekhate parbo jodi task successfully add hoy tahole amra user ke success message dekhate parbo and jodi task add na hoy tahole amra user ke error message dekhate parbo

           context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
           return render(request,self.template_name,context)





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
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES,instance=task.details)# for Post
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



class UpdateTask(UpdateView):
    model=Task
    form_class=TaskModelForm
    template_name="task_form.html"
    context_object_name="task"
    pk_url_kwarg="id"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task_form']=self.get_form()#task_form er data nia aslam
        
        if hasattr(self.object,'details') and self.object.details:
            context["task_detail_form"]=TaskDetailModelForm(instance=self.object.details)

        else:
            context["task_detail_form"]=TaskDetailModelForm()
        return context
    
    def post(self,request,*args,**kwargs):
        self.object=self.get_object()#specific task er data nia aslam
        task_form=TaskModelForm(request.POST,instance=self.object)# for Post

        task_detail_form=TaskDetailModelForm(request.POST,request.FILES,instance=getattr(self.object,'details',None))# for Post

        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task updated Successfully")

            return redirect('update_task', self.object.id)
        return redirect('update_task', self.object.id)

    




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




 


#use aggregate function to calculate max, min, count and average of a field in a queryset
@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_tasks(request):  
    # task_count=Task.objects.aggregate(num_count=Count('id'))#count ar kaj hosse database theke task er total count nia aslam
    
    projects=Project.objects.annotate(task_count=Count('task')).order_by('task_count')#annotate ar kaj hosse database theke project er sathe task er count nia aslam karon amra annotate use korechi and task_set ar vitore task er data thake karon amra prefetch_related use korechi and task_set ar vitore task er data thake tai amra project er sathe task er count nia aslam
    return render(request,"show_task.html",{"projects":projects})


#variables for list of decorators
view_project_decorators=[login_required,permission_required('projects.view_project', login_url='no-permission')]

@method_decorator(view_project_decorators, name='dispatch')
class ViewProjects(ListView):
    model=Project
    template_name="show_task.html"
    context_object_name="projects"

    def get_queryset(self):

        return Project.objects.annotate(task_count=Count('task')).order_by('task_count')




@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def task_details(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choice=Task.STATUS_CHOICES
    if request.method=="POST":
        selected_status=request.POST.get("task_status")
        print(selected_status)
        task.status=selected_status
        task.save()
        messages.success(request,"Task status updated successfully")
        return redirect('task-details',task.id)
    return render(request,"task_details.html",{"task":task,"status_choice":status_choice})



class TaskDetailView(DetailView):
    model=Task
    template_name="task_details.html"
    context_object_name="task"
    pk_url_kwarg="task_id"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)#{'task': <Task: Task object (1)>}
        context["status_choice"]=Task.STATUS_CHOICES#{'task': <Task: Task object (1)>, 'status_choice': [('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')]}
        return context
    

    def post(self,request,*args,**kwargs):
        task=self.get_object()#specific task er data nia aslam
        selected_status=request.POST.get("task_status")#form theke selected status nia aslam
        task.status=selected_status#task er status update korechi
        task.save()#task er data save korechi
        messages.success(request,"Task status updated successfully")#success message dekhatechi
        return redirect('task-details',task.id)#redirect korechi task details page a jekhane task er updated status dekhabe



@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')





