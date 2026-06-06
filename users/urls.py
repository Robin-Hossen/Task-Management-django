from django.urls import path

from users.views import admin_dashboard, create_group, group_list, sign_up, sign_in,sign_out, activate_user_account,admin_dashboard,assign_role,ProfileView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

urlpatterns = [
    path('sign-up/',sign_up,name="sign-up"),
    # path('sign-in/',sign_in,name="sign-in"),
    path('sign-in/',LoginView.as_view(),name="sign-in"),
    path('sign-out/',sign_out,name="logout"),
    path('admin/assign-role/<int:user_id>/', assign_role, name="assign-role"),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('activate/<int:user_id>/<str:token>/', activate_user_account),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),

]