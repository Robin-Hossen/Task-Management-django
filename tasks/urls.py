from django.urls import path
from tasks.views import dashboard, employee_dashboard, manager_dashboard,task,create_task, view_tasks,update_task,delete_task


urlpatterns = [
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('dashboard/', dashboard),
    path('task/', task),
    path('create_task/',create_task,name='create_task'),
    path('view_tasks/',view_tasks),
    path('update_task/<int:id>/',update_task,name='update_task'),
    path('delete_task/<int:id>/',delete_task,name='delete_task')
]
