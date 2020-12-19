from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def welcome(request):
   return render(request,"welcome.html")


def login(request):
    return render(request,"sign-in.html")

def signup(request):
   return render(request,"sign-in.html")