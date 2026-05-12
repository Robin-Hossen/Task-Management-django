
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class RegistrationForm(UserCreationForm):
        class Meta:
                model = User
                fields = ['username','first_name','last_name','email','password1','password2']
        def __init__(self, *args, **kwargs):
            super(UserCreationForm, self).__init__(*args, **kwargs)
            for fieldname in ['username','password1','password2']:
                self.fields[fieldname].help_text= None



class CustomRegistrationForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','confirm_password']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", password1):
            raise forms.ValidationError("Password must contain at least one number")

        if not re.search(r"[!@#$%^&*]", password1):
            raise forms.ValidationError("Password must contain at least one special character")

        return password1



    def clean(self):#non field level validation 
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data 
    
    def clean_email(self): #email field level validation   

        email=self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():# checking if email already exists in database or not
            raise forms.ValidationError("Email already exists")
        return email



    
        
        



        

    
    
