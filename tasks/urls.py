from django.urls import path
from tasks.views import dashboard, manager_dashboard, user_dashboard,task,create_task


urlpatterns = [
    path('manager_dashboard/', manager_dashboard,),
    path('user_dashboard/', user_dashboard),
    path('dashboard/', dashboard),
    path('task/', task),
    path('create_task/',create_task)
]
