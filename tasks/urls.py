from django.urls import path
from tasks.views import dashboard, manager_dashboard, user_dashboard,task


urlpatterns = [
    path('manager_dashboard/', manager_dashboard,),
    path('user_dashboard/', user_dashboard),
    path('dashboard/', dashboard),
    path('task/', task),
]
