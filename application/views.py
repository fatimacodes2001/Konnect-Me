from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from operator import itemgetter
from django.urls import reverse
from itertools import chain

import mysql.connector

from .models import RegularProfile,Page,PageFollowsPage,PageFollowsProfile,ProfileFollowsPage,ProfileFollowsProfile,Status,Job
from .forms import *
from .imageTools import *
from PIL import Image, ImageOps
from pathlib import Path
import os
from django.template import RequestContext
mail = ""


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "konnect_me"
)

mycursor = mydb.cursor()






# Create your views here.

def welcome(request):
   return render(request,"welcome.html")


def login(request):


   return render(request,"sign-in.html")




def signup(request):
   return render(request,"sign-in.html")



def feed(request):
      global mail


      try:
         mail = request.POST["email"]
         email = mail
         password = request.POST["password"]
      except:
         email = mail
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

         val = False
         for key in suggestions:
            if key==email:
               val = True
               break
         
         if val==True:
            suggestions.pop(email)










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
            statuses.sort(key = lambda x: x.date,reverse=True)


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
               profs = PageFollowsProfile.objects.filter(follower_page_email=each.followed_page_email.email)
               page_s = PageFollowsPage.objects.filter(follower_email=each.followed_page_email.email)

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
                  p = Page.objects.get(email= obj.followed_page_email.email)
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

            value = False
            for key in suggestions:
               if key==email:
                  value = True
                  break
            if value==True:
               suggestions.pop(email)




            context = dict()
            context['email'] = email
            context['names'] = names
            context['suggestions'] = suggestions
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
      email = mail
      date = datetime.now()

      try:
         reg_pro = RegularProfile.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,regular_profile_email=reg_pro,caption=caption,num_likes=0,num_shares=0,location=location,date=date)
         post.save()


      except RegularProfile.DoesNotExist:
         page = Page.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,page_email=page,caption=caption,num_likes=0,num_shares=0,location=location,date=date)
         post.save()

      return redirect(reverse('feed'))

def addjob(request):

   
      email = mail

      title = request.POST.get('jobtitle')
      qualification = request.POST.get('qualification')
      location = request.POST.get('job_location')
      vacant = request.POST['vacant']
      contact = request.POST['contact']
      cost = request.POST['price1']
      cost = int(cost)
      type_job = request.POST['type']
      time = request.POST['time']
      time = int(time)
      desc = request.POST['description']
      date = datetime.now()
      page = Page.objects.get(email=email)
      job = Job(page_email=page,qualification=qualification,num_hours=time,num_posts=vacant,salary=cost,contact_detail=contact,location=location,postdate=date,description=desc)
      job.save()
      return redirect(reverse('feed'))



def search(request):
   email = mail
   emails = []
   persons = []
   pages = []

   query = request.POST.get("mainsearch")
   query = str(query)

   query_l = ""
   if len(query.split())>1:
      query_l = query.split()[1]
   else:
      query_l = query.split()[0]


   q = '''select email from page where
title like "'''+query+'''%" or companyType like "'''+query+'''%"
union
select email from regular_profile
where firstName like "'''+ query.split()[0]+'''%" or lastName
like "'''+query_l+'''%"
union select regular_profile.email
from regular_profile inner join interests
where interest like "'''+query+'''%"
union select regular_profile.email
from regular_profile inner join skills
where skill like "'''+query+'''%"'''

   mycursor.execute(q)
   context = dict()

   myresult = mycursor.fetchall()

   for each in myresult:
      emails.append(each[0])
   print(emails)
   for each in emails:
      try:
         person = RegularProfile.objects.get(email=each)
         persons.append(person)

      except RegularProfile.DoesNotExist:

         page = Page.objects.get(email=each)
         pages.append(page)
   print(len(persons))

   context['name'] = RegularProfile.objects.get(email=email).firstname + " " + RegularProfile.objects.get(email=email).lastname
   context['people'] = persons
   context['pages'] = pages
   return render(request,"search.html",context=context)












def searchjobs(request):

   email = request.session['email']
   ids = []

   query = request.POST.get("search")

   q = '''select * from job where type like "'''+query+'''%"
or description like "%'''+query+'''%" or qualification like"'''+query+'''%"
union
select job.* from job inner join page
on page.email = job.page_email
where title like "'''+query+'''%"'''

   mycursor.execute(q)
   jobs_list = []
   page = dict()
   myresult = mycursor.fetchall()

   for each in myresult:
      ids.append(each[0])




   for each in ids:
      job = Job.objects.get(job_id=each)
      jobs_list.append(job)
      obj = Page.objects.get(email=job.page_email.email)
      page[job.page_email] = obj.title

   context = dict()
   context['jobs'] = jobs_list
   context['name'] = RegularProfile.objects.get(email=email).firstname + " " + RegularProfile.objects.get(email=email).lastname
   context['page'] = page

   return render(request,"searchjobs.html",context=context)







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




def signup_two(request):

    print(request.POST)
    print("signup_two")
    print(request.GET)

    if request.method == 'POST':
        form = TestForm(request.POST,request.FILES)
        if form.is_valid():
            img = Image.open(request.FILES['image'])
            croppedImage = resizer(crop(img),250)
            status_id = form.cleaned_data['status_id']
            album = form.cleaned_data['album']
            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(album.regular_profile_email.email))
            if not USER_IMAGES.exists():
                os.mkdir(USER_IMAGES)
            LOCATION =  Path(USER_IMAGES,str(status_id)+".jpg")
            croppedImage = croppedImage.convert('RGB')
            croppedImage.save(LOCATION, optimize=True, quality=85)
    else:
        form = TestForm()

    exp1 = {"name":"Full Stack End Developer","detail":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."}
    return render(request,"sign-up.html",{'form':form,"exp":exp1})

def index(request):
   return render(request,"index.html")



def profile(request):


    email = "abc@abc.com"


    profile_pic = Photos.objects.filter(regular_profile_email = email, update_id = 1).order_by('update_id')
    profile = RegularProfile.objects.filter(email = email).first()

    update = Status.objects.filter(regular_profile_email = email).order_by('update_id')

    skills = Skills.objects.filter(email = email).order_by('skill')
    interests = Interests.objects.filter(email = email).order_by('interest')


    follower_profiles = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_email')
    follower_pages = PageFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_page_email')


    followers = list(chain(follower_profiles,follower_pages))

    profile_followings = ProfileFollowsProfile.objects.filter(follower_email = email).order_by('followed_profile_email')
    page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = email).order_by('page_email')

    followings = list(chain(profile_followings,page_followings))

    non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.exclude(email__in = [object.page_email.email for object in page_followings])))


    followed_follower_profiles = ProfileFollowsProfile.objects.filter(follower_email = email, followed_profile_email__in = [object.follower_email for object in follower_profiles] ).order_by('follower_email')
    followed_followers_pages = ProfileFollowsPage.objects.filter(regular_profile_email = email, page_email__in = [object.follower_page_email for object in follower_pages] ).order_by('page_email')


    followed_followers = list(chain(followed_follower_profiles,followed_followers_pages))
    unfollowed_followers = list(
                        chain(
                        ProfileFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_email__in = [object.followed_profile_email for object in followed_follower_profiles])
                        ,
                        PageFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_page_email__in = [object.page_email for object in followed_followers_pages])
                        )
                        )

    up1 = RegularProfile.objects.exclude(email__in = [object.follower_email.email for object in follower_profiles])
    up2 = Page.objects.exclude(email__in = [object.follower_page_email.email for object in follower_pages])
    up3 = chain(up1,up2)
    up4 = list(up3)


    print("\n\n\n")
    print("......")
    for f in follower_profiles:
        print(f.followed_profile_email.email)
    print("\n\n\n")
    print("......")
    for f in up1:
        print(f)

    print("\n\n\n")
    print("......")
    for f in up2:
        print(f)

    print("\n\n\n")
    print("......")
    for f in follower_profiles:
        print(f)

    print("\n\n\n")
    print("......")
    for f in follower_pages:
        print(f)

    print("\n\n\n")
    print("......")
    for f in followings:
        print(f)

    print("\n\n\n")
    print("......")
    for f in non_followings:
        print(f)

    print("\n\n\n")
    print("end")
    albums = Album.objects.filter(regular_profile_email = email).order_by('name')

    # suggestions = RegularProfile.objects.filter(email__in = non_followings.values_list('email', flat=True)).exclude(email = email).order_by("?")[:6]

    # self_follow = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_profile_email')

    MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
    PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))


    if not MAIN.exists():

        os.mkdir(MAIN)


    if not PROFILE_PICTURES.exists():

        profile_pics = Album.objects.create(regular_profile_email=RegularProfile.objects.filter(email = email).first(),name="Profile Pictures",num_photos=0)

        os.mkdir(PROFILE_PICTURES)


    # print(request.POST)
    # print(request.GET)
    # print()


    if request.method == 'POST':


        if "update_id" in request.POST:

            update_id = request.POST.get("update_id")

            clicked_update = Status.objects.filter(regular_profile_email = email, update_id = update_id).first()


            if "num_likes" in request.POST:

                update_likes =  request.POST.get("num_likes")

                liker = ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).first()


                if liker:

                    ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).delete()

                    clicked_update.num_likes = update_likes;

                    clicked_update.save()

                else :

                    liker = ProfileLikesStatus.objects.create(update_id = update_id, regular_profile_email = profile, status_like_id = update_id)

                    clicked_update.num_likes = update_likes;

                    clicked_update.save()


            if "num_shares" in request.POST:

                update_shares =  request.POST.get("num_shares")

                sharer = ProfileSharesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, share_id = update_id).first()


                if not sharer:

                    sharer = ProfileSharesStatus.objects.create(update_id = update_id, regular_profile_email = profile, share_id = update_id)

                    clicked_update.num_shares = update_shares;

                    clicked_update.save()


            likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')
            shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


        if "make-album" in request.POST:

            form = AlbumForm(request.POST,request.FILES)


            if form.is_valid():

                album = form.save()

                album.regular_profile_email = RegularProfile.objects.filter(email = email).first()
                album.num_photos = 0

                album.save()

                name = form.cleaned_data['name']

                album_id = album.album_id

                USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(album_id))


                if not USER_IMAGES.exists():

                    os.mkdir(USER_IMAGES)


        if "album_id" in request.POST:

            album_id = request.POST.get("album_id")

            clicked_album = Album.objects.filter(album_id = album_id).first()

            album_name = clicked_album.name

            photos = Photos.objects.filter(regular_profile_email = email, album_id = album_id).order_by('update_id')

            form = PhotoForm()


        if "make-image" in request.POST:

            form = PhotoForm(request.POST,request.FILES)


            if form.is_valid():

                album = Album.objects.filter(album_id = album_id).first()

                photo = Image.open(request.FILES['photo'])

                photof = form.save(commit=False)

                album.num_photos += 1

                album.save()

                photof.regular_profile_email = profile
                photof.album = album
                photof.status_id = 10
                photof.num_likes = 0
                photof.num_lhares = 0
                photof.location = ""+profile.city+" "+profile.state


                if album.name == "Profile Pictures":

                    croppedPhoto = resizer(crop(photo),170)
                    croppedPhoto35 = resizer(crop(photo),35)

                    USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(profile.email),str(profile.email))


                    if not USER_IMAGES.exists():

                        os.mkdir(USER_IMAGES)

                    form.save()

                    LOCATION =  Path(USER_IMAGES,str(profile.email)+".jpg")
                    LOCATION35 =  Path(USER_IMAGES,str(profile.email)+"35.jpg")

                    croppedPhoto = croppedPhoto.convert('RGB')
                    croppedPhoto35 = croppedPhoto35.convert('RGB')

                    croppedPhoto.save(LOCATION, optimize=True, quality=85)
                    croppedPhoto35.save(LOCATION35, optimize=True, quality=70)

                else:

                    croppedPhoto = resizer(photo,1000)
                    USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(profile.email),str(album_id))


                    if not USER_IMAGES.exists():

                        os.mkdir(USER_IMAGES)

                    form.save()

                    LOCATION =  Path(USER_IMAGES,str(photof.update_id)+".jpg")

                    croppedPhoto = croppedPhoto.convert('RGB')
                    croppedPhoto.save(LOCATION, optimize=True, quality=85)


                    # image.regular_profile_email = RegularProfile.objects.filter(email = email).first()
                    # image.num_photos = 0
                    # image.save()
                    # name = form.cleaned_data['name']
                    # album_id = album.album_id
                    # USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(album_id))
                    # if not USER_IMAGES.exists():
                    #     os.mkdir(USER_IMAGES)

        else:

            # form = AlbumForm()
            form = PhotoForm()


    else:

        # form = AlbumForm()
        form = PhotoForm()


    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(request)
    print(request.POST)
    print(request.GET)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


    if request.is_ajax():

        album_id = request.GET.get('album_id')

        # update_id = request.GET.get('update_id')

        clicked_album = Album.objects.filter(regular_profile_email=email,album_id=album_id).first()
        photos = Photos.objects.filter(regular_profile_email=email,album_id=album_id).order_by("update_id")

        # clicked_update = Status.objects.filter(regular_profile_email = email, update_id = update_id).first()
        # likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')

        template = 'album.html'


        if 'update_id' in request.GET:

            update_id = request.GET.get('update_id')


            if 'num_likes' in request.GET:

                template = 'likes.html'


            elif 'num_shares' in request.GET:

                template = 'shares.html'


            else:

                clicked_photo = Photos.objects.filter(regular_profile_email=email,update_id=update_id).first()
                template = 'album.html'


    else:

        template = 'user-profile.html'


    album_id = request.GET.get('album_id')
    update_id = request.GET.get('update_id')


    clicked_album = Album.objects.filter(regular_profile_email=email,album_id=album_id).first()
    clicked_update = Status.objects.filter(regular_profile_email = email, update_id = update_id).first()


    photos = Photos.objects.filter(regular_profile_email=email,album_id=album_id).order_by("update_id")

    all_photos = Photos.objects.filter(regular_profile_email=email).order_by("?")[:9]


    shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')

    # likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')
    # likesp = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')

    likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
            ,PageLikesStatus.objects.filter(update = clicked_update)))

    album_cover = Photos.objects.filter(regular_profile_email=email).order_by("album_id").distinct()


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
       profs = PageFollowsProfile.objects.filter(follower_page_email=each.followed_page_email.email)
       page_s = PageFollowsPage.objects.filter(follower_email=each.followed_page_email.email)

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
          p = Page.objects.get(email= obj.followed_page_email.email)
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


    context = dict()

    context['profile'] = profile

    context['status'] = update

    context['skills'] = skills
    context['interests'] = interests

    context['followers'] = followers

    context['followed_followers'] = followed_followers
    context['unfollowed_followers'] = unfollowed_followers

    context['followings'] = followings
    context['non_followings'] = non_followings

    context['form'] = form

    context['albums'] = albums
    context['album_id'] = album_id

    context['photos'] = photos
    context['all_photos'] = all_photos

    context['clicked_album'] = clicked_album
    context['album_cover'] = album_cover

    context['suggestions'] = suggestions

    context['shares'] = shares
    context['likes'] = likes


    return render(request,template,context)
