from threading import Thread
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from yahoo_fin.stock_info import *
from django.views.decorators.csrf import csrf_exempt
import time
import queue


@login_required(login_url='signin')
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            return HttpResponse("Your Password Does not match!!!")
        elif User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken!!")
        else:
            my_user = User.objects.create_user(username=username, email=email, password=password)
            my_user.save()
            return redirect('signin')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect !!!")
    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('index')


def contact_us(request):
    return render(request, 'contact_us.html')


def stockpicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'stockpicker.html', {'stockpicker': stock_picker})


@csrf_exempt
def stocktracker(request):
    if request.method == "POST":
        stockpicker = request.POST.getlist('stock_picked')
        print(stockpicker)
        data = {}
        available_stocks = tickers_nifty50()
        for i in stockpicker:
            if i in available_stocks:
                pass
            else:
                return HttpResponse("Stock not Present!!")
        n_threads = len(stockpicker)
        thread_list = []
        que = queue.Queue()
        start = time.time()
        for i in range(n_threads):
            thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}),
                            args=(que, stockpicker[i]))
            thread_list.append(thread)
            thread_list[i].start()

        for thread in thread_list:
            thread.join()

        while not que.empty():
            result = que.get()
            data.update(result)
        end = time.time()
        time_taken = end - start
        print(time_taken)

        print(data)
        return render(request, 'stocktracker.html', {'data': data})
