
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
def register_view(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save();login(request,user);return redirect('/')
    return render(request,'register.html',{'form':form})
def login_view(request):
    form=AuthenticationForm(request,data=request.POST or None)
    if form.is_valid():
        login(request,form.get_user());return redirect('/')
    return render(request,'login.html',{'form':form})
def logout_view(request):
    logout(request);return redirect('/')
