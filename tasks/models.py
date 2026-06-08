from django.db import models
from django.conf import settings



# Create your models here.
class Task(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("IN_PROGRESS","In Progress"),
        ("COMPLETED","Completed")
    ]
#foriegn key ar jonne  ("")use kora hoise karon parent upore thake
    project=models.ForeignKey("Project",on_delete=models.CASCADE, default=1)
    # assigned_to=models.ManyToManyField('Employee',related_name='tasks')
    assigned_to=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='tasks')
    title=models.CharField(max_length=500)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title #django te __str__ method use kore amra model er object ke string hisabe represent korte pari. jemon amra jodi Task.objects.all() kori tahole amra task er title dekhte parbo karon __str__ method e amra title return korechi. jodi __str__ method na thake tahole amra task er object ke string hisabe represent korte parbo na and amra task er id dekhte parbo.


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
    task=models.OneToOneField(
            Task,
            on_delete=models.DO_NOTHING,
            related_name='details')
    asset=models.ImageField(upload_to='tasks_asset', blank=True, null=True, default='https://media.istockphoto.com/id/2173059563/vector/coming-soon-image-on-white-background-no-photo-available.jpg?s=612x612&w=0&k=20&c=v0a_B58wPFNDPULSiw_BmPyhSNCyrP_d17i2BPPyDTk=')
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes=models.TextField(blank=True,null=True)#blank and null er mane hocche user jodi notes na dey tahole oita blank thakbe and null thakbe database a

    def __str__(self):
        return f"Details for Task: {self.task.title} with priority {self.get_priority_display()}"

#many to one relation
#project parent and Task hosse tar child
#beacuse project na thakle task kivabe thakbe

#model make korar por foreign key add korte hobe 
class Project(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    start_date=models.DateField()

    def __str__(self):
        return self.name


#many to many
#task= onekgula employee akta task
#employee = onekgula task ar jonno assign ase





