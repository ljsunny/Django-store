from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  
        fields = ['name', 'price', 'image']
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control","name":"name","id":"name","placeholder":"Enter the  Name label"}),
            'price': forms.TextInput(attrs={"class":"form-control","name":"price","id":"price","placeholder":0}),
            'image':forms.FileInput(attrs={"type":"file","class":"form-control","name":"image","id":"image"})
        }

class RegisterForm(forms.Form):
    uname = forms.CharField(required=True, 
                            label = "Enter User Name", 
                            widget=forms.TextInput(attrs={"class":"form-control", "name":"uname","placeholder:":"Enter User Name"}))
    password = forms.CharField(required=True, 
                        label = "Enter User Password", 
                        widget=forms.PasswordInput(attrs={"class":"form-control", "name":"password","placeholder:":"Enter User Password"}))
    email = forms.CharField(required=True, 
                    label = "Enter User Email", 
                    widget=forms.EmailInput(attrs={"class":"form-control", "name":"email","placeholder:":"Enter User Email"}))
    fname = forms.CharField(required=True, 
                            label = "Enter User First Name", 
                            widget=forms.TextInput(attrs={"class":"form-control", "name":"fname","placeholder:":"Enter User First Name"}))
    lname = forms.CharField(required=True, 
                            label = "Enter User Last Name", 
                            widget=forms.TextInput(attrs={"class":"form-control", "name":"lname","placeholder:":"Enter User Last Name"}))
    

class LoginForm(forms.Form):
    uname = forms.CharField(required=True, 
                            label = "Enter User Name", 
                            widget=forms.TextInput(attrs={"class":"form-control", "name":"uname","placeholder:":"Enter User Name"}))
    password = forms.CharField(required=True, 
                        label = "Enter User Password", 
                        widget=forms.PasswordInput(attrs={"class":"form-control", "name":"password","placeholder:":"Enter User Password"}))
    
class ChangePassForm(forms.Form):
    email = forms.CharField(required=True, 
                label = "Enter User Email", 
                widget=forms.EmailInput(attrs={"class":"form-control", "name":"email","placeholder:":"Enter User Email"}))
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "name":"old_password","placeholder:":"Enter User Password"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "name":"new_password","placeholder:":"Enter User Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "name":"confirm_password","placeholder:":"Enter User Password"}))