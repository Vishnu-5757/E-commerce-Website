from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid:
            form.save()
            return render(request,'users/created.html')
    form=NewUserForm()
    context={
        'form':form,
    }

    return render(request,'users/register.html',context)

@login_required
def profile(request):
    return render(request,'users/profile.html')


def create(request):
    if request.method=='POST':
        contact=request.POST.get('contact')
        place=request.POST.get('place')
        image=request.FILES['upload']
        user=request.user
        profile=Profile(user=user,contact_number=contact,place=place,image=image)
        profile.save()
    return render(request,'users/createprofile.html')


def created(request):
    return render(request,'users/created.html')


