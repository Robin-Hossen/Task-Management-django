from django.urls import path
from tasks.views import dashboard, employee_dashboard, manager_dashboard,task,create_task, task_details, view_tasks,update_task,delete_task,CreateTask, TaskDetailModelForm


urlpatterns = [
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='user-dashboard'),
    #path('dashboard/', dashboard),
    path('task/', task),
    # path('create_task/',create_task,name='create_task'),
    path('create_task/',CreateTask.as_view(),name='create_task'),
    path('view_tasks/',view_tasks),
    path('task/<int:task_id>/details/', task_details, name='task-details'),
    path('update_task/<int:id>/',update_task,name='update_task'),
    path('delete_task/<int:id>/',delete_task,name='delete_task'),
    path('dashboard', dashboard, name='dashboard'),
]
