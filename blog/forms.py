from django import forms
from django.forms import widgets
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.core.exceptions import *

# user registration form
class SignUpFrom(UserCreationForm):
    class Meta:
        model = Author
        fields = ('username', "email", "is_superuser")
        labels = {"username":"Username", "email":"Email", "is_superuser": "Admin"}
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}),
            "email":forms.EmailInput(attrs={"class":"form-control", "placeholder":"Email"}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password" 
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password" 
        self.fields["email"].required = True  
    

# user login / authetication form        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["password"].label = "Password"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Username" 
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = "Password" 
 
# catagory form        
class CatagoriesForm(forms.ModelForm):
    
    class Meta:
        model = Catagorie 
        fields = ("catagory",)
        labels = {"catagory":"Catagory"}
        widgets = {"catagory":forms.TextInput(attrs={"placeholder":"Catagory" ,"class":"form-control"})}
    
# post form
class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "desc", "catagory","image")
        labels = {
            "title":"Title",
            "desc":"Description",
            "image":"Image",
            "catagory":"Catagory"
            }
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control", "placeholder":"Title"}),
            "desc":forms.Textarea(attrs={"class":"form-control", "placeholder":"Descrption", "rows":4}),
            "catagory":forms.Select(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
            
            }
        
# update author form
class UpdateAuthorForm(UserChangeForm):
    class Meta:
        model = Author
        fields = ('username', "email", "first_name", "last_name", "is_superuser")
        labels = {"username":"Username",
                  "email":"Email",
                  "first_name":"First Name",
                  "last_name":"Last Name",
                  "is_superuser": "Admin"
                }
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}),
            "email":forms.EmailInput(attrs={"class":"form-control", "placeholder":"Email"}),
            "first_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}),
            "last_name":forms.TextInput(attrs={"class":"form-control", "placeholder": "Last Name"}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True 

class ChangePassword(PasswordChangeForm):
    class Meta:
        model = Author
        fields = ("old_password", "new_password1", "new_password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control" 
 
