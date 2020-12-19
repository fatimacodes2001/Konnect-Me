from django.contrib import admin
from django.urls import path, include
from application import views


urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
]
