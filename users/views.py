
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib.auth.tokens import default_token_generator 
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView
from django.urls import reverse_lazy



#test function to check if user is admin
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            print("Password and confirm password do not match")    
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active=False
            user.save()    
            messages.success(request, "Account created successfully. Please check your email to activate your account.")
            return redirect('sign-in')
        else:   
            print("Form is not valid") 
    return render(request,"registration/register.html",{"form":form})



def sign_in(request):
    form=LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,"registration/login.html",{"form":form})


class CustomLoginView(LoginView):

    form_class = LoginForm
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()
        
        
        
class ChangePassword(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/Change_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "A password reset email has been sent to your email address.Please check your email.")
        return super().form_valid(form)
    

@login_required
def sign_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('sign-in')
    

def activate_user_account(request, user_id, token):
    try:
         user = User.objects.get(id=user_id)
        #  print("User found: ", user.username)
         if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
         else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    

@user_passes_test(is_admin, login_url='no-permission')    
def admin_dashboard(request):
    users=User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(),to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.groups_name=user.all_groups[0].name
        else:
            user.groups_name='No Group Assigned'
    return render(request, 'admin/dashboard.html', {'users': users})  



@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()  # Clear existing roles
            user.groups.add(role)  # Assign new role
            messages.success(request, f"Group '{role.name}' assigned to user '{user.username}' successfully.")
            user.save()
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})    
    



@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            
            group=form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})




class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name']=user.get_full_name()
        context['member_since']=user.date_joined
        context['last_login']=user.last_login
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['protocol']= 'https' if self.request.is_secure() else 'http'
        context['domain']= self.request.get_host()
        
        return context
    

    def form_valid(self, form):
        messages.success(self.request, "A password reset email has been sent to your email address.Please check your email.")
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been reset successfully.")
        return super().form_valid(form)
    


