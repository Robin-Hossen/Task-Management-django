from django.urls import path

from users.views import CustomPasswordResetConfirmView, admin_dashboard, create_group, group_list, sign_up, sign_in,sign_out, activate_user_account,admin_dashboard,assign_role,ProfileView,ChangePassword,CustomPasswordResetView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView


urlpatterns = [
    path('sign-up/',sign_up,name="sign-up"),
    # path('sign-in/',sign_in,name="sign-in"),
    path('sign-in/',LoginView.as_view(),name="sign-in"),
    # path('sign-out/',sign_out,name="logout"),
    path('sign-out/',LogoutView.as_view(),name="logout"),
    path('admin/assign-role/<int:user_id>/', assign_role, name="assign-role"),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('activate/<int:user_id>/<str:token>/', activate_user_account),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('Change_password/', ChangePassword.as_view(), name='change-password'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    

]