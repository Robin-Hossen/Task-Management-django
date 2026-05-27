
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm,AssignRoleForm,CreateGroupForm
from django.contrib.auth.tokens import default_token_generator 
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch

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