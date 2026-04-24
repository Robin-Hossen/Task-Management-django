from django.db import models

# Create your models here.
class Task(models.Model):
#foriegn key ar jonne  ("")use kora hoise karon parent upore thake
    project=models.ForeignKey("Project",on_delete=models.CASCADE, default=1)
    assigned_to=models.ManyToManyField("Employee",related_name='tasks')
    title=models.CharField(max_length=500)
    description=models.TextField()
    due_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


#One To One Relation 
#Task ar sate Task_details ar ,,Task parent and Task_details child
#from tasks.models import Task
# t=Task(title="low priority task",description="motamuti chole",due_date="2026-04-23")
#Query
#Task.objects.get(id=2) django te
#task=Task.objects.get(id=1)
#TaskDetail.objects.create(task=task1,assigned_to=kolim,priority=l)
#select * from where id=2 raw sql a
class TaskDetail(models.Model):
    HIGH="H"
    MEDIUM="M"
    LOW="L"
    PRIORITY_OPTIONS=(
        (HIGH,'High'),(MEDIUM,'Medium'),(LOW,'Low')
    )
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name='details')
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)




#many to one relation
#project parent and Task hosse tar child
#beacuse project na thakle task kivabe thakbe

#model make korar por foreign key add korte hobe 
class Project(models.Model):
    name=models.CharField(max_length=200)
    start_date=models.DateField()


#many to many
#task= onekgula employee akta task
#employee = onekgula task ar jonno assign ase

class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)



