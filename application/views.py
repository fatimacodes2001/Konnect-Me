from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime

from operator import itemgetter
from django.urls import reverse

import mysql.connector
from .models import RegularProfile,Page,PageFollowsPage,PageFollowsProfile,ProfileFollowsPage,ProfileFollowsProfile,Status,Job






# Create your views here.

def welcome(request):
   return render(request,"welcome.html")


def login(request):
      

   return render(request,"sign-in.html")




def signup(request):
   return render(request,"sign-in.html")



def feed(request):


      try:
         email = request.POST["email"]
         password = request.POST["password"]
      except:
         email = request.session["email"]
         password = request.session["password"]


      try:
         person = RegularProfile.objects.get(email=email,password=password)

         request.session['email'] = email
         request.session['password'] = password


         fname = person.firstname
         lname = person.lastname
         num_followers = person.num_followers
         request.session["email"] = email

         followed_pages = len(ProfileFollowsPage.objects.filter(regular_profile_email=email))
         followed_profiles = len(ProfileFollowsProfile.objects.filter(follower_email=email))

         pages = ProfileFollowsPage.objects.filter(regular_profile_email=email)
         profiles = ProfileFollowsProfile.objects.filter(follower_email=email)

         statuses = []
         names = dict()
        


         for each in profiles:
            stats = Status.objects.filter(regular_profile_email=each.followed_profile_email)
            obj = RegularProfile.objects.get(email=each.followed_profile_email.email)
            
            

            for post in stats:
               statuses.append(post)
               names[post.update_id] = obj.firstname + " " + obj.lastname
               




         for each in pages:
            stats = Status.objects.filter(page_email=each.page_email)

            obj = Page.objects.get(email = each.page_email.email)



            for post in stats:
               statuses.append(post)
               names[post.update_id] = obj.title
               
                  

         #Ordering by date
         statuses.sort(key = lambda x: x.date,reverse=True)


         #suggestions
         f_profiles = []
         f_pages = []

         followed1 = ProfileFollowsPage.objects.filter(regular_profile_email=email)
         for each in followed1:
            f_pages.append(each.page_email.email)


         followed2 = ProfileFollowsProfile.objects.filter(follower_email=email)
         for each in followed2:
            f_profiles.append(each.followed_profile_email.email)

         sugges1 = []
         sugges2 = []

         for each in followed1:
            profs = PageFollowsProfile.objects.filter(follower_page_email=each.page_email.email)
            page_s = PageFollowsPage.objects.filter(follower_email=each.page_email.email)

            for obj in profs:
               profile = RegularProfile.objects.get(email=obj.followed_profile_email.email)
               if profile.email not in f_profiles:
                  sugges1.append(profile)
            
            for obj in page_s:
               p = Page.objects.get(email= obj.followed_page_email.email)
               if p.email not in f_pages:
                  sugges2.append(p)



         for each in followed2:
            profs = ProfileFollowsProfile.objects.filter(follower_email=each.followed_profile_email.email)
            page_s = ProfileFollowsPage.objects.filter(regular_profile_email=each.followed_profile_email.email)

            for obj in profs:
               profile = RegularProfile.objects.get(email=obj.followed_profile_email.email)
               if profile.email not in f_profiles:
                  sugges1.append(profile)
            
            for obj in page_s:
               p = Page.objects.get(email= obj.page_email.email)
               if p.email not in f_pages:
                  sugges2.append(p)

         sugges1.sort(key = lambda x: x.num_followers,reverse=True)
         
         sugges2.sort(key = lambda x: x.numfollowers,reverse=True)
         


         suggestions = dict()
         if len(sugges1)>3:
            sugges1 = sugges1[0:3]
         if len(sugges2)>3:
            sugges2 = sugges2[0:3]

         for each in sugges1:
            suggestions[each.email] = each.firstname+" "+each.lastname

         for each in sugges2:
            suggestions[each.email] = each.title

         print(suggestions)

            





   


         num_followed = followed_pages+followed_profiles
         context = dict()
         context['email'] = email
         context["status"] = statuses 
         context['fname'] = fname
         context['names'] = names
         context['suggestions'] = suggestions
         context['lname'] = lname
         context['name'] = fname+" "+lname
         context['followers'] = num_followers
         context['followed'] = num_followed


         return render(request,"index.html",context=context)



      except RegularProfile.DoesNotExist:


         try:
            page = Page.objects.get(email=email,password=password)
            name = page.title
            num_followers = page.numfollowers
            
               

            followed_pages = len(PageFollowsPage.objects.filter(follower_email=email))
            followed_profiles = len(PageFollowsProfile.objects.filter(follower_page_email=email))
            
            num_followed = followed_pages+followed_profiles


            pages = PageFollowsPage.objects.filter(follower_email=email)
            profiles = PageFollowsProfile.objects.filter(follower_page_email=email)

            statuses = []
            names = dict()


            for each in profiles:
               stats = Status.objects.filter(regular_profile_email=each.followed_profile_email.email)
               obj = RegularProfile.objects.get(email=each.followed_profile_email.email)
            

               for post in stats:
                  statuses.append(post)
                  names[post.update_id] = obj.firstname + " " + obj.lastname



            for each in pages:
               stats = Status.objects.filter(page_email=each.followed_page_email.email)
       
               obj = Page.objects.get(email = each.followed_page_email.email)

               for post in stats:
                  statuses.append(post)
                  names[post.update_id] = obj.title

            #Ordering by date
            '''statuses.sort(key = lambda x: x.date,reverse=True)


            #suggestions
            f_profiles = []
            f_pages = []

            followed1 = PageFollowsPage.objects.filter(follower_email=email)
            for each in followed1:
               f_pages.append(each.followed_page_email.email)


            followed2 = PageFollowsProfile.objects.filter(follower_page_email=email)
            for each in followed2:
               f_profiles.append(each.followed_profile_email.email)

            sugges1 = []
            sugges2 = []

            for each in followed1:
               profs = PageFollowsProfile.objects.filter(follower_page_email=each.page_email.email)
               page_s = PageFollowsPage.objects.filter(follower_email=each.page_email.email)

               for obj in profs:
                  profile = RegularProfile.objects.get(email=obj.followed_profile_email.email)
                  if profile.email not in f_profiles:
                     sugges1.append(profile)
               
               for obj in page_s:
                  p = Page.objects.get(email= obj.followed_page_email.email)
                  if p.email not in f_pages:
                     sugges2.append(p)



            for each in followed2:
               profs = ProfileFollowsProfile.objects.filter(follower_email=each.followed_profile_email.email)
               page_s = ProfileFollowsPage.objects.filter(regular_profile_email=each.followed_profile_email.email)

               for obj in profs:
                  profile = RegularProfile.objects.get(email=obj.followed_profile_email.email)
                  if profile.email not in f_profiles:
                     sugges1.append(profile)
               
               for obj in page_s:
                  p = Page.objects.get(email= obj.page_email.email)
                  if p.email not in f_pages:
                     sugges2.append(p)

            sugges1.sort(key = lambda x: x.num_followers,reverse=True)
            
            sugges2.sort(key = lambda x: x.numfollowers,reverse=True)
            


            suggestions = dict()
            if len(sugges1)>3:
               sugges1 = sugges1[0:3]
            if len(sugges2)>3:
               sugges2 = sugges2[0:3]

            for each in sugges1:
               suggestions[each.email] = each.firstname+" "+each.lastname

            for each in sugges2:
               suggestions[each.email] = each.title

            print(suggestions)'''




            context = dict()
            context['email'] = email
            context['names'] = names
            #context['suggestions'] = suggestions
            context['status'] = statuses
            context['name'] = name
            context['followers'] = num_followers
            context['followed'] = num_followed
            return render(request,"indexpage.html",context=context)



         except  Page.DoesNotExist:

            messages.info(request,"Check Email or Password")
            print("ERROR")
            return redirect('login')

            
      return render(request,"index.html")




def add(request):

   if request.method == 'POST':



      caption = request.POST['caption']
      location = request.POST['location']
      email = request.session['email']

      try:
         reg_pro = RegularProfile.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,regular_profile_email=reg_pro,caption=caption,num_likes=0,num_shares=0,location=location,date="2020-11-11")
         post.save()
      
      
      except RegularProfile.DoesNotExist:
         page = Page.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,page_email=page,caption=caption,num_likes=0,num_shares=0,location=location,date="2020-11-11")
         post.save()

      return redirect(reverse('feed'))




def jobs(request):
      email = request.session['email']
      pages = ProfileFollowsPage.objects.filter(regular_profile_email=email)
      jobs = []
      page = dict()

      for each in pages:
         jobs_list = Job.objects.filter(page_email=each.page_email)
         
         for job in jobs_list:
            jobs.append(job)
            
            obj = Page.objects.get(email=job.page_email.email)
            print(obj)

            print(obj.title)
            page[job.page_email] = obj.title

      context = dict()
      context['jobs'] = jobs
      context['name'] = RegularProfile.objects.get(email=email).firstname + " " + RegularProfile.objects.get(email=email).lastname
      context['page'] = page

      return render(request,"jobs.html",context=context)
      