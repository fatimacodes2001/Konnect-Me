from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from operator import itemgetter
import mysql.connector
from .models import RegularProfile,Page,PageFollowsPage,PageFollowsProfile,ProfileFollowsPage,ProfileFollowsProfile

# Create your views here.

def welcome(request):
   return render(request,"welcome.html")


def login(request):
      

   return render(request,"sign-in.html")




def signup(request):
   return render(request,"sign-in.html")

   

def feed(request):
   if request.method == "POST":
      email = request.POST["email"]
      password = request.POST["password"]

      try:
         person = RegularProfile.objects.get(email=email,password=password)
         fname = person.firstname
         lname = person.lastname
         num_followers = person.num_followers
         request.session["email"] = email

         followed_pages = len(ProfileFollowsPage.objects.filter(regular_profile_email=email))
         followed_profiles = len(ProfileFollowsProfile.objects.filter(follower_email=email))

         num_followed = followed_pages+followed_profiles
         context = dict()
         context['email'] = email
         context['fname'] = fname
         context['lname'] = lname
         context['name'] = fname+" "+lname
         context['followers'] = num_followers
         context['followed'] = num_followed
         return render(request,"index.html",context=context)



      except:
         try:
            page = Page.objects.get(email=email,password=password)
            name = page.title
            num_followers = page.numfollowers

            followed_pages = len(PageFollowsPage.objects.filter(follower_email=email))
            followed_profiles = len(PageFollowsProfile.objects.filter(follower_page_email=email))
            request.session["email"] = email

            num_followed = followed_pages+followed_profiles
            context = dict()
            context['email'] = email
            context['name'] = name
            context['followers'] = num_followers
            context['followed'] = num_followed
            return render(request,"index.html",context=context)



         except:

            messages.info(request,"Check Email or Password")
            return redirect('login')
   return render(request,"index.html")