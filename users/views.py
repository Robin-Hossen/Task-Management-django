
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm,AssignRoleForm
from django.contrib.auth.tokens import default_token_generator 
from django.contrib import messages
from users.forms import LoginForm


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
    
def admin_dashboard(request):
    users=User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})   


def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()  # Clear existing roles
            user.groups.add(role)  # Assign new role
            messages.success(request, f"Role '{role.name}' assigned to user '{user.username}' successfully.")
            user.save()
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})    
    

    


