from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
@login_required(login_url='signup')
def home(request):
    return render(request,'home.html')


def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        
        if password != cpassword:
            return HttpResponse("Your Password Does not match!!!")
        elif User.objects.filter(username=username).exists():
                return HttpResponse("Username already taken!!")
        else:    
            my_user=User.objects.create_user(username=username, email=email, password=password)
            my_user.save()
            return redirect('signin')
        #print(username, email, password, cpassword)
    return render(request,'signup.html')


def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            return HttpResponse("Username or Password is incorrect !!!")
    return render(request,'signin.html')


def signout(request):
    index(request)
    return redirect(request,'index.html')
