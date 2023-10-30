from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms


class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'focus:outline-none','placeholder':'123@gmail.com'}))
    phone=forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none','placeholder':'+91 8592091233'}))
    username=forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none','placeholder':'Username'}))
    password1=forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none','placeholder':'****'}))
    password2=forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none','placeholder':'****'}))

    class Meta:
        model=User
        fields=("username","phone","email","password1","password2")

    def save(self,commit=True):
        user=super(NewUserForm,self).save(commit=False) 
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user    

