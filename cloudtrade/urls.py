from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup.html', views.signup, name='signup'),
    path('signin.html', views.signin, name='signin'),
    path('signout.html', views.signout, name='signout'),
    path('home.html', views.home, name='home'),
]