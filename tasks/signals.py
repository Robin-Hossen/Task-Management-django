
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task


# email signals  
# 
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':  # Check if employees were added to the task
       
        assigned_emails=[emp.email for emp in instance.assigned_to.all()]
        send_mail(
                'New Task Assigned',
                f'You have been assigned a new task: {instance.title}',
                'hossenrobin215@gmail.com',
                assigned_emails,
                fail_silently=False,
            )
        
        

@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        print("Associated TaskDetail deleted successfully.")
