from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
from app.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def register(request):
    userform=UserForm()
    profileform=ProfileForm()
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid() and PD.is_valid():
            us=UD.save(commit=False)
            pw=UD.cleaned_data['password']
            us.set_password(pw)
            us.save()
            ps=PD.save(commit=False)
            ps.user=us
            ps.save()
            send_mail('Registration',
            'Thanks For registration',
            'likithnani567@gmail.com',
            [us.email],fail_silently=False)
            return HttpResponse('Registration is successfull')


    
    d={'userform':userform,'profileform':profileform}
    return render(request,'register.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        return render(request,'home.html',context={'username':username})
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('please enter correct user details')


    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile(request):
    username=request.session['username']
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)

    return render(request,'profile.html',context={'user':user,'profile':profile})

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session['username']
        password=request.POST['password']
        user=User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return HttpResponse('password is changed successfully')



    return render(request,'change_password.html')


def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.filter(username=username)
        if user:
            user[0].set_password(password)
            user.save()
            return HttpResponse('reset of password done Successfully')
        else:
            return HttpResponse('please eneter correct user')
    return render(request,'forgot_password.html')


