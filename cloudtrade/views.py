from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request,'home.html')


def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('signup')
        if not password:
            messages.error(request, "Password is required.")
            return redirect('signup')
        
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Your account has been created.")
            return redirect('signin')
        except IntegrityError:
            messages.error(request, 'Username already exists')
            return redirect('signup')
    return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) or None
        if user is not None:
            login(request, user)
            return render(request,"index.html", )
        else:
            messages.error(request,"Username or Password does not match")
            return redirect('home')
    
    return render(request,'signin.html')




def signout(request):
    logout(request)
    return redirect('home')
