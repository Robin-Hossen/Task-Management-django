
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User,Permission,Group
import re
from tasks.forms import djangoFormMixin


class RegistrationForm(UserCreationForm):
        class Meta:
                model = User
                fields = ['username','first_name','last_name','email','password1','password2']
        def __init__(self, *args, **kwargs):
            super(UserCreationForm, self).__init__(*args, **kwargs)
            for fieldname in ['username','password1','password2']:
                self.fields[fieldname].help_text= None



class CustomRegistrationForm(djangoFormMixin, forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField(required=True)

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
    

class LoginForm( djangoFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(djangoFormMixin,forms.Form):
        role=forms.ModelChoiceField(
            queryset=Group.objects.all(), 
            empty_label="Select Role",
            )

class CreateGroupForm(djangoFormMixin,forms.ModelForm):
        permissions=forms.ModelMultipleChoiceField(
                queryset=Permission.objects.all(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                label=" Assign Permissions"

        )
        class Meta:
                model=Group
                fields=['name','permissions']


class CustomPasswordChangeForm(djangoFormMixin,PasswordChangeForm):
    pass   


class CustomPasswordResetForm(djangoFormMixin,PasswordResetForm):
    pass 

               
class CustomPasswordResetConfirmForm(djangoFormMixin,SetPasswordForm):
    pass                


class EditProfileForm(djangoFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    bio=forms.CharField(widget=forms.Textarea, required=False,label="Bio")
    profile_image=forms.ImageField(required=False,label="Profile Image")

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)


        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit)
        #save userprofile jodi thake
        if self.userprofile:
             self.userprofile.bio=self.cleaned_data.get('bio')
             self.userprofile.profile_image=self.cleaned_data.get('profile_image')
             if commit:
                self.userprofile.save()
        if commit:
            user.save()  

        return user        


        


    
        
        



        

    
    
