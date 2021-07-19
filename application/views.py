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
import re
from .imageTools import *
from PIL import Image, ImageOps
from pathlib import Path
import os
from django.template import RequestContext
mail = ""


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tuchapax-999",
  database = "konnect_me"
)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'






mycursor = mydb.cursor()


def signup(request):
    global mail
    print("Called")

    if request.method == 'POST':
        print("Sign Up")
        if (re.search(regex,request.POST["email"])):

            mycursor.execute("SELECT email FROM page")
            emails = mycursor.fetchall()

            mycursor.execute("SELECT email FROM regular_profile")
            emails2 = mycursor.fetchall()

            exists = False
            for email in emails:
                print("exists")
                if (request.POST["email"] == email[0]):
                    exists = True

            for email in emails2:
                print("exists")
                if (request.POST["email"] == email[0]):
                    exists = True

            if (not exists):
                if (request.POST["password"] == request.POST["confirm-password"]):

                    email = request.POST["email"]
                    mail = email
                    password = request.POST["password"]

                    request.session['email'] = email
                    request.session['password'] = password

                    name = request.POST["name"].split(" ", 1)
                    try:
                        firstName = name[0]
                        lastName = name[1]
                    except:
                        lastName = ''

                    mycursor.execute("INSERT INTO regular_profile (email, password, firstName, lastName) VALUES (%s, %s, %s, %s)",
                                    (email, password, firstName, lastName))
                    print("committed")
                    mydb.commit()
                    return redirect("/application/create")
                else:
                    messages.success(request, "Passwords Do Not Match!")
                    return redirect("/signup")
            else:
                messages.success(request, "Email Already Exists! Please Sign In.")
                return redirect("/signup")
        else:
            messages.success(request, "Invalid Email!")
            return redirect("/signup")
    else:
        return render(request, "sign-in.html")






def signup2(request):
    global mail
    if request.method == 'POST':
        if (re.search(regex,request.POST["email"])):

            mycursor.execute("SELECT email FROM page")
            emails = mycursor.fetchall()

            mycursor.execute("SELECT email FROM regular_profile")
            emails2 = mycursor.fetchall()


            exists = False
            for email in emails:
                if (request.POST["email"] == email[0]):
                    exists = True

            for email in emails2:
                if (request.POST["email"] == email[0]):
                    exists = True

            if (not exists):
                if (request.POST["password"] == request.POST["confirm-password"]):

                    email = request.POST["email"]
                    password = request.POST["password"]
                    mail = email

                    request.session['email'] = email
                    request.session['password'] = password

                    name = request.POST["company-name"]

                    mycursor.execute("INSERT INTO page (email, password, title) VALUES (%s, %s, %s)",
                                    (email, password, name))
                    mydb.commit()

                    return redirect("/application/createpage")
                else:
                    messages.success(request, "Passwords Do Not Match!")
                    return redirect("/signup")
            else:
                messages.success(request, "Email Already Exists! Please Sign In.")
                return redirect("/signup")
        else:
            messages.success(request, "Invalid Email!")
            return redirect("/signup")
    else:
        return render(request, "sign-in.html")





def create(request):
    email = mail

    if request.method == 'POST':
        gender = request.POST["gender"]

        # mail = request.session['email']
        interests = [request.POST["interest1"], request.POST["interest2"], request.POST["interest3"]]

        skills = [request.POST["skill1"], request.POST["skill2"], request.POST["skill3"]]

        mycursor.execute("UPDATE regular_profile SET gender = %s, dob = %s, about_you = %s, work_profile = %s, city = %s, state = %s, p_grad = %s, u_grad = %s, high_school = %s, Further_education = %s WHERE email = %s",
                        (gender, request.POST["birthday"], request.POST["about"], request.POST["workprof"], request.POST["city"], request.POST["state"],
                        request.POST["school"], request.POST["ugrad"], request.POST["pgrad"], request.POST["edu"], email))

        mycursor.execute("DELETE FROM interests WHERE email = %s", (email,))
        for interest in interests:
            mycursor.execute("REPLACE INTO interests (email, interest) VALUES (%s, %s)", (email, interest))

        mycursor.execute("DELETE FROM skills WHERE email = %s", (email,))
        for skill in skills:
                mycursor.execute("REPLACE INTO skills (email, skill) VALUES (%s, %s)", (email, skill))

        # Code for uploading an image
        mydb.commit()
        email = mail
        regular_profile = RegularProfile.objects.filter(email = email).first()

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))

        if not MAIN.exists():
            os.mkdir(MAIN)

        profile_pics = []

        if not PROFILE_PICTURES.exists():
            print("DOES NOT")
            print(regular_profile)
            profile_pics = Album.objects.create(regular_profile_email = regular_profile,name="Profile Pictures",num_photos=0)
            print("Album: ", profile_pics)
            os.mkdir(PROFILE_PICTURES)




        album = profile_pics

        photo = Image.open(r'media\defaultdp.png')

        album.num_photos += 1

        album.save()



        if album.name == "Profile Pictures":

            if Photos.objects.filter(album = album):
                Photos.objects.filter(album = album).delete()

            croppedPhoto = resizer(crop(photo),170)
            croppedPhoto35 = resizer(crop(photo),37)

            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(email))

            if not USER_IMAGES.exists():

                os.mkdir(USER_IMAGES)

            Photos.objects.create(album = album,status_id = 10, regular_profile_email = regular_profile,caption = "NEW PROFILE PICTURE",date=datetime.now(),num_likes=0,num_shares=0, city = regular_profile.city, state=regular_profile.state)


            LOCATION =  Path(USER_IMAGES,str(email)+".jpg")
            LOCATION35 =  Path(USER_IMAGES,str(email)+"35.jpg")

            croppedPhoto = croppedPhoto.convert('RGB')
            croppedPhoto35 = croppedPhoto35.convert('RGB')

            croppedPhoto.save(LOCATION, optimize=True, quality=85)
            croppedPhoto35.save(LOCATION35, optimize=True, quality=70)


        return redirect("/application/feed")
    else:
        print("Redirecting")
        return render(request, "create-profile.html")

def createpage(request):

    email = mail
    print("Email:", email)
    if request.method == 'POST':

        mycursor.execute("UPDATE page SET companyType = %s, aboutYou = %s, city = %s, state = %s WHERE email = %s",
                        (request.POST["type"], request.POST["about"], request.POST["city"], request.POST["state"], email))

        mydb.commit()
        print("EMAIL:",email)
        page = Page.objects.filter(email = email).first()
        print(page.email)

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))
        profile_pics = []

        if not MAIN.exists():
            os.mkdir(MAIN)


        if not PROFILE_PICTURES.exists():
            profile_pics = Album.objects.create(page_email = page,name="Profile Pictures",num_photos=0)
            os.mkdir(PROFILE_PICTURES)

        else:
            profile_pics = Album.objects.get(page_email = page,name="Profile Pictures",num_photos=0)



        album = profile_pics

        photo = Image.open(r'media\defaultdp.png')

        album.num_photos += 1

        album.save()



        if album.name == "Profile Pictures":

            if Photos.objects.filter(album = album):
                Photos.objects.filter(album = album).delete()

            croppedPhoto = resizer(crop(photo),170)
            croppedPhoto35 = resizer(crop(photo),37)

            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(email))

            if not USER_IMAGES.exists():

                os.mkdir(USER_IMAGES)

            Photos.objects.create(album = album,status_id = 10, page_email =page,caption = "NEW PROFILE PICTURE",date=datetime.now(),num_likes=0,num_shares=0, city = page.city, state=page.state)


            LOCATION =  Path(USER_IMAGES,str(email)+".jpg")
            LOCATION35 =  Path(USER_IMAGES,str(email)+"35.jpg")

            croppedPhoto = croppedPhoto.convert('RGB')
            croppedPhoto35 = croppedPhoto35.convert('RGB')

            croppedPhoto.save(LOCATION, optimize=True, quality=85)
            croppedPhoto35.save(LOCATION35, optimize=True, quality=70)


        return redirect("/application/feed")
    else:
        return render(request, "create-page.html")


def editprofile(request):
    email = mail

    if request.method == 'POST':
        gender = request.POST["gender"]


        interests = [request.POST["interest1"], request.POST["interest2"], request.POST["interest3"]]

        skills = [request.POST["skill1"], request.POST["skill2"], request.POST["skill3"]]

        mycursor.execute("UPDATE regular_profile SET firstName = %s, lastName = %s, gender = %s, dob = %s, about_you = %s, work_profile = %s, city = %s, state = %s, p_grad = %s, u_grad = %s, high_school = %s, Further_education = %s WHERE email = %s",
                        (request.POST["fname"], request.POST["lname"], gender, request.POST["birthday"], request.POST["about"], request.POST["workprof"], request.POST["city"], request.POST["state"],
                        request.POST["school"], request.POST["ugrad"], request.POST["pgrad"], request.POST["edu"], email))

        mycursor.execute("DELETE FROM interests WHERE email = %s", (email,))
        for interest in interests:
            mycursor.execute("REPLACE INTO interests (email, interest) VALUES (%s, %s)", (email, interest))


        mycursor.execute("DELETE FROM skills WHERE email = %s", (email,))
        for skill in skills:
            mycursor.execute("REPLACE INTO skills (email, skill) VALUES (%s, %s)", (email, skill))

        mydb.commit()



        messages.success(request, "Saved Profile Successfully!")
        return redirect("/application/editprofile")
    else:
        context = {}
        mycursor.execute("SELECT * FROM regular_profile WHERE email = %s", (email,))
        myresult = mycursor.fetchall()

        interests = []
        mycursor.execute("SELECT * FROM interests WHERE email = %s", (email,))
        myresult2 = mycursor.fetchall()
        for result in myresult2:
            if(not result[1].isspace() and result[1]):
                interests.append(result[1])

        skills = []
        mycursor.execute("SELECT * FROM skills WHERE email = %s", (email,))
        myresult3 = mycursor.fetchall()
        for result in myresult3:
            if(not result[1].isspace() and result[1]):
                skills.append(result[1])

        context['password'] = myresult[0][1]
        context['firstName'] = myresult[0][2]
        context['lastName'] = myresult[0][3]

        gender = myresult[0][4]
        if gender == "M":
            sex = 'Male'
        elif gender == 'F':
            sex = 'Female'
        else:
            sex = 'Other'

        print("Gender:", gender)
        context['gender'] = sex
        context['gender2'] = gender

        context['dob'] = myresult[0][5]
        context['about_you'] = myresult[0][6]
        context['work_profile'] = myresult[0][7]
        context['city'] = myresult[0][8]
        context['state'] = myresult[0][9]
        context['p_grad'] = myresult[0][10]
        context['u_grad'] = myresult[0][11]
        context['highschool'] = myresult[0][12]
        context['furtheredu'] = myresult[0][13]

        i = 1
        for interest in interests:
            context['interest'+ str(i)] = interest
            i += 1

        i = 1
        for skill in skills:
            context['skill'+ str(i)] = skill
            i += 1


        return render(request, "edit-profile.html", context)

def changepassword(request):
    email  = mail
    if request.method == 'POST':

        mycursor.execute("SELECT password from regular_profile WHERE email = %s", (email,))
        passwords = mycursor.fetchall()
        password = passwords[0][0]

        if (request.POST['old-password'] == password):
            if (request.POST["new-password"] == request.POST["repeat-password"]):
                mycursor.execute("UPDATE regular_profile SET password = %s WHERE email = %s", (request.POST["new-password"], email))
                mydb.commit()

                request.session['password'] = request.POST["new-password"]

                messages.error(request, "Password Changed Successfully!")
                return redirect("/application/changepassword")
            else:
                messages.error(request, "Password Reset Failed! New Passwords Do Not Match!")
                return redirect("/application/changepassword")

        else:
            messages.error(request, "Password Reset Failed! Invalid Password Entered.")
            return redirect("/application/changepassword")

    else:
        return render(request, "change-password.html")

def editpage(request):
    email = mail
    if request.method == 'POST':

        mycursor.execute("UPDATE page SET title = %s, companyType = %s, aboutYou = %s, city = %s, state = %s WHERE email = %s",
                        (request.POST["title"], request.POST["type"], request.POST["about"], request.POST["city"], request.POST["state"], email))

        mydb.commit()

        messages.success(request, "Saved Page Successfully!")
        return redirect("/application/editpage")
    else:
        context = {}
        mycursor.execute("SELECT * FROM page WHERE email = %s",(email,))
        myresult = mycursor.fetchall()

        context['password'] = myresult[0][1]
        context['type'] = myresult[0][3]
        context['title'] = myresult[0][4]
        context['about_you'] = myresult[0][5]
        context['city'] = myresult[0][6]
        context['state'] = myresult[0][7]

        return render(request, "edit-page.html", context)

def changepassword2(request):
    email  = mail;
    if request.method == 'POST':

        mycursor.execute("SELECT password from page WHERE email = %s", (email,))
        passwords = mycursor.fetchall()
        password = passwords[0][0]

        if (request.POST['old-password'] == password):
            if (request.POST["new-password"] == request.POST["repeat-password"]):
                mycursor.execute("UPDATE page SET password = %s WHERE email = %s", (request.POST["new-password"], email))
                mydb.commit()

                request.session['password'] = request.POST["new-password"]

                messages.error(request, "Password Changed Successfully!")
                return redirect("/application/changepassword")
            else:
                messages.error(request, "Password Reset Failed! New Passwords Do Not Match!")
                return redirect("/application/changepassword")

        else:
            messages.error(request, "Password Reset Failed! Invalid Password Entered.")
            return redirect("/application/changepassword")

    else:
        return render(request, "change-password2.html")


def changedp(request):
    if request.method == 'POST':

        email = request.session['email']
        regular_profile = RegularProfile.objects.filter(email = email).first()

        form = GeeksForm(request.POST, request.FILES)
        if form.is_valid():


            album = Album.objects.filter(regular_profile_email = regular_profile,name = "Profile Pictures").first()

            photo = Image.open(request.FILES.get('img')) #gets image from form

            album.num_photos += 1

            album.save()

            if album.name == "Profile Pictures":

                if Photos.objects.filter(album = album):
                    Photos.objects.filter(album = album).delete()
                    album.num_photos -= 1

                    #PROFILE PHOTO CREATION

                croppedPhoto = resizer(crop(photo),170)
                croppedPhoto35 = resizer(crop(photo),37)

                USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(email))

                if not USER_IMAGES.exists():

                    os.mkdir(USER_IMAGES)

                Photos.objects.create(album = album,status_id=10, regular_profile_email = regular_profile,caption = "NEW PROFILE PICTURE",date=datetime.now(),num_likes=0,num_shares=0, city = regular_profile.city, state=regular_profile.state)

                LOCATION =  Path(USER_IMAGES,str(email)+".jpg")
                LOCATION35 =  Path(USER_IMAGES,str(email)+"35.jpg")

                croppedPhoto = croppedPhoto.convert('RGB')
                croppedPhoto35 = croppedPhoto35.convert('RGB')

                croppedPhoto.save(LOCATION, optimize=True, quality=85)
                croppedPhoto35.save(LOCATION35, optimize=True, quality=70)

            messages.error(request, "Profile Picture Changed Sucessfully!")
            return redirect("/application/changedp")


        else:
            messages.error(request, "Failed to Change Profile Picture!.")
            return redirect("/application/changedp")

    else:
        context = {}
        form = GeeksForm()
        context['form'] = form
        return render(request, "change-profile-picture.html", context)

def changedp2(request):
    if request.method == 'POST':

        email = mail
        page = Page.objects.filter(email = email).first()

        form = GeeksForm(request.POST, request.FILES)
        if form.is_valid():


            album = Album.objects.filter(page_email = page,name = "Profile Pictures").first()

            photo = Image.open(request.FILES.get('img')) #gets image from form

            album.num_photos += 1

            album.save()

            if album.name == "Profile Pictures":

                if Photos.objects.filter(album = album):
                    Photos.objects.filter(album = album).delete()

                    #PROFILE PHOTO CREATION

                croppedPhoto = resizer(crop(photo),170)
                croppedPhoto35 = resizer(crop(photo),37)

                USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(email))

                if not USER_IMAGES.exists():

                    os.mkdir(USER_IMAGES)

                Photos.objects.create(album = album,status_id = 10, page_email =page,caption = "NEW PROFILE PICTURE",date=datetime.now(),num_likes=0,num_shares=0, city = page.city, state=page.state)


                LOCATION =  Path(USER_IMAGES,str(email)+".jpg")
                LOCATION35 =  Path(USER_IMAGES,str(email)+"35.jpg")

                croppedPhoto = croppedPhoto.convert('RGB')
                croppedPhoto35 = croppedPhoto35.convert('RGB')

                croppedPhoto.save(LOCATION, optimize=True, quality=85)
                croppedPhoto35.save(LOCATION35, optimize=True, quality=70)

            messages.error(request, "Profile Picture Changed Sucessfully!")
            return redirect("/application/changedp2")


        else:
            messages.error(request, "Failed to Change Profile Picture!.")
            return redirect("/application/changedp2")

    else:
        context = {}
        form = GeeksForm()
        context['form'] = form
        return render(request, "change-profile-picture2.html", context)







# Create your views here.

def welcome(request):
   return redirect("/signup")


def login(request):

   return redirect("/signup")






def feed(request):
      global mail


      try:
         mail = request.POST["emailin"]
         email = mail
         password = request.POST["passwordin"]
      except:
         email = mail
         password = request.session["password"]


      try:
         q = '''select * from regular_profile
         where email="'''+email+ '''"and password ="'''+password+'''"'''
         mycursor.execute(q)
         res = mycursor.fetchall()
         if len(res)==0:
            raise RegularProfile.DoesNotExist("No Profile")

         person = RegularProfile.objects.get(email=email,password=password)

         request.session['email'] = email
         request.session['password'] = password
         profile = RegularProfile.objects.get(email=email)


         fname = person.firstname
         lname = person.lastname
         num_followers = person.num_followers
         request.session["email"] = email

         followed_pages = len(ProfileFollowsPage.objects.filter(regular_profile_email=email))
         followed_profiles = len(ProfileFollowsProfile.objects.filter(follower_email=email))



         pages = ProfileFollowsPage.objects.filter(regular_profile_email=email)
         profiles = ProfileFollowsProfile.objects.filter(follower_email=email)


         follower_profiles = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_email')
         follower_pages = PageFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_page_email')

         albums = Album.objects.filter(regular_profile_email = email).order_by('name')


         MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
         print(MAIN)
         PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))
         print(PROFILE_PICTURES)


         if not MAIN.exists():

            os.mkdir(MAIN)


         if not PROFILE_PICTURES.exists():

            profile_pics = Album.objects.create(regular_profile_email=RegularProfile.objects.filter(email = email).first(),name="Profile Pictures",num_photos=0)

            os.mkdir(PROFILE_PICTURES)




         CHOICES = []
         for album in albums:
            choice = (album.album_id,album.name)
            CHOICES.append(choice)
         CHOICES = tuple(CHOICES)


         followers = list(chain(follower_profiles,follower_pages))

         profile_followings = ProfileFollowsProfile.objects.filter(follower_email = email).order_by('followed_profile_email')
         page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = email).order_by('page_email')

         followings = list(chain(profile_followings,page_followings))


         non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                        ,Page.objects.exclude(email__in = [object.page_email.email for object in page_followings])))


         followed_follower_profiles = ProfileFollowsProfile.objects.filter(follower_email = email, followed_profile_email__in = [object.follower_email for object in follower_profiles] ).order_by('follower_email')
         followed_followers_pages = ProfileFollowsPage.objects.filter(regular_profile_email = email, page_email__in = [object.follower_page_email for object in follower_pages] ).order_by('page_email')


         followed_followers = list(chain(followed_follower_profiles,followed_followers_pages))
         unfollowed_followers = list(chain(ProfileFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_email__in = [object.followed_profile_email for object in followed_follower_profiles])
                            ,PageFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_page_email__in = [object.page_email for object in followed_followers_pages])))


         statuses = []
         names = dict()
         template = "index.html"
         form = PhotoForm(CHOICES)





         if request.method == 'POST':
            profile  = RegularProfile.objects.get(email=email)



            if "update_id" in request.POST:

                  update_id = request.POST.get("update_id")

                  clicked_update = Status.objects.filter(update_id = update_id).first()
                  likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')
                  shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')




                  if "num_likes" in request.POST:

                     update_likes =  request.POST.get("num_likes")

                     liker = ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).first()


                     if liker:

                        ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).delete()

                        clicked_update.num_likes = update_likes

                        clicked_update.save()

                     else :

                        liker = ProfileLikesStatus.objects.create(update_id = update_id, regular_profile_email = profile, status_like_id = update_id)

                        clicked_update.num_likes = update_likes


                        clicked_update.save()


                  if "num_shares" in request.POST:

                     update_shares =  request.POST.get("num_shares")

                     sharer = ProfileSharesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, share_id = update_id).first()


                     if not sharer:
                        date = datetime.now()
                        sharer = ProfileSharesStatus.objects.create(update_id = update_id, regular_profile_email = profile, share_id = update_id,date=date)

                        clicked_update.num_shares = update_shares

                        status = Status.objects.get(update_id = update_id)
                        status.num_shares += 1
                        status.save()

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



            if "make-image" in request.POST:

                     form = PhotoForm(CHOICES,request.POST,request.FILES)

                     if form.is_valid():

                        album = Album.objects.filter(album_id = album_id).first()

                        photo = Image.open(request.FILES.get('photo')) #gets image from form

                        photof = form.save(commit=False)

                        album.num_photos += 1

                        album.save()

                        photof.regular_profile_email = profile

                        photof.album = album
                        photof.date = datetime.now()

                        photof.status_id = 10
                        photof.num_likes = 0
                        photof.num_shares = 0
                        photof.city = profile.city
                        photof.state = profile.state
                        photof.save()


                        if album.name == "Profile Pictures":

                            if Photos.objects.filter(album = album):
                                Photos.objects.filter(album = album).delete()

                            #PROFILE PHOTO CREATION

                            croppedPhoto = resizer(crop(photo),170)
                            croppedPhoto35 = resizer(crop(photo),37)

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

                            #PROFILE PHOTO CREATION END

                            #Remove else for updating only profile pic
                        else:

                            croppedPhoto = resizer(photo,1000)
                            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(profile.email),str(album_id))


                            if not USER_IMAGES.exists():

                                os.mkdir(USER_IMAGES)

                            form.save()

                            LOCATION =  Path(USER_IMAGES,str(photof.update_id)+".jpg")

                            croppedPhoto = croppedPhoto.convert('RGB')
                            croppedPhoto.save(LOCATION, optimize=True, quality=85)


            else:

                    # form = AlbumForm()
                    form = PhotoForm(CHOICES)











         if request.is_ajax:


             if 'type' in request.GET:

                if request.GET.get('type') == "followers" :

                    template = "followers.html"

                if request.GET.get('type') == "followings" :

                    template = "followings.html"

             if "type" in request.POST:

                if request.POST.get("type") == "page":

                    if "followed_email" in request.POST:

                        followed_email = request.POST.get("followed_email")
                        followed_page = Page.objects.filter(email = followed_email).first()

                        if not ProfileFollowsPage.objects.filter(page_email = followed_page , regular_profile_email = profile ):
                            follow = ProfileFollowsPage.objects.create(page_email = followed_page , regular_profile_email = profile )
                            print("followed "+followed_email)

                    if "un_followed_email" in request.POST:

                        un_followed_email= request.POST.get("un_followed_email")

                        if ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = email):
                            unfollow = ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = email).delete()
                            print("unfollowed "+un_followed_email)

                if request.POST.get("type") == "profile":

                    if "followed_email" in request.POST:

                        followed_email = request.POST.get("followed_email")
                        followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                        if not ProfileFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_email = profile):
                            follow = ProfileFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_email = profile)
                            print("followed "+followed_email)

                    if "un_followed_email" in request.POST:

                        un_followed_email= request.POST.get("un_followed_email")

                        if ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = email):
                            unfollow = ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = email).delete()
                            print("unfollowed "+un_followed_email)



             if 'update_id' in request.GET:

                update_id = request.GET.get('update_id')
                likes = ProfileLikesStatus.objects.filter(update = update_id).order_by('regular_profile_email')
                shares = ProfileSharesStatus.objects.filter(update = update_id).order_by('regular_profile_email')


             if 'num_likes' in request.GET:

                template = 'likes.html'


             elif 'num_shares' in request.GET:

                template = 'shares.html'

         else:

                template = 'index.html'














         photo_add = dict()
         for each in profiles:
            stats = Status.objects.filter(regular_profile_email=each.followed_profile_email)
            obj = RegularProfile.objects.get(email=each.followed_profile_email.email)
            pics = Photos.objects.filter(regular_profile_email=each.followed_profile_email)


            for post in stats:
               statuses.append(post)
               names[post.update_id] = obj.firstname + " " + obj.lastname

            for pic in pics:
                   statuses.append(pic)
                   names[pic.update_id] = obj.firstname + " " + obj.lastname
                   alb_id = pic.album.album_id
                   up_id = pic.update_id
                   add = "media/"+obj.email+"/"+str(alb_id)+"/"+str(up_id)+".jpg"
                   photo_add[up_id] = add



         for each in profiles:
             share = ProfileSharesStatus.objects.filter(regular_profile_email=each.followed_profile_email)
             p_shared = ProfileSharesPhotos.objects.filter(regular_profile_email=each.followed_profile_email)

             for sh in share:
                 statuses.append(sh)

             for p in p_shared:
                    ph = Photos.objects.get(update_id = p.update.update_id )
                    s_mail = ""

                    if(ph.regular_profile_email is None):
                        s_mail = ph.page_email.email
                    else:
                        s_mail = ph.regular_profile_email.email


                    up_id = ph.update_id
                    alb_id = ph.album.album_id
                    add = "media/"+str(s_mail)+"/"+str(alb_id)+"/"+str(up_id)+".jpg"
                    photo_add[up_id] = add

                    statuses.append(p)





         for each in pages:
            stats = Status.objects.filter(page_email=each.page_email)
            photos_p = Photos.objects.filter(page_email=each.page_email)

            obj = Page.objects.get(email = each.page_email.email)



            for post in stats:
               statuses.append(post)
               names[post.update_id] = obj.title

            for pic in photos_p:
                   statuses.append(pic)
                   names[pic.update_id] = obj.title
                   up_id = pic.update_id
                   alb_id = pic.album.album_id
                   add = "media/"+obj.email+"/"+str(alb_id)+"/"+str(up_id)+".jpg"


         update_id = request.GET.get('update_id')

         clicked_update = Status.objects.filter(update_id = update_id).first()


         shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')

         likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                ,PageLikesStatus.objects.filter(update = clicked_update)))




         statuses.sort(key = lambda x: x.date,reverse=True)

         profile_followings = ProfileFollowsProfile.objects.filter(follower_email = email).order_by('followed_profile_email')
         page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = email).order_by('page_email')

         followings = list(chain(profile_followings,page_followings))


         non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.exclude(email__in = [object.page_email.email for object in page_followings])))





         #suggestions
         profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in profile_followings])]
         page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.page_email for email in page_followings])]

         profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in profile_followings])]
         page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.page_email for email in page_followings])]

         profile_suggestion = set(chain(profile_following_profile,page_following_profile))
         page_suggestion = set(chain(profile_following_page,page_following_page))

         for profiles in profile_followings:
            profile_suggestion.discard(profiles.follower_email)
            profile_suggestion.discard(profiles.followed_profile_email)
         for pages in page_followings:
            profile_suggestion.discard(pages.regular_profile_email)
            page_suggestion.discard(pages.page_email)

         profile_suggestion = list(profile_suggestion)
         page_suggestion = list(page_suggestion)

         profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
         page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

         if len(profile_suggestion)>3:
            profile_suggestion = profile_suggestion[0:3]
         if len(page_suggestion)>3:
            page_suggestion = page_suggestion[0:3]

         suggestions = list(chain(profile_suggestion,page_suggestion))

         profile = RegularProfile.objects.get(email=email)
         num_followed = followed_pages+followed_profiles

         context = dict()
         context['email'] = email
         context['form'] = form
         context["status"] = statuses
         context['profile'] = profile
         context['fname'] = fname
         context['names'] = names
         context['pic_add'] = photo_add
         context['suggestions'] = suggestions
         context['lname'] = lname
         context['name'] = fname+" "+lname
         context['followed_followers'] = followed_followers
         context['unfollowed_followers'] = unfollowed_followers


         context['profile'] = profile
         context['likes'] = likes
         context['shares'] = shares
         context['followings'] = followings
         context['non_followings'] = non_followings
         context['followers'] = followers






         return render(request,template,context=context)



      except RegularProfile.DoesNotExist:


         try:
            q = '''select * from page
         where email="'''+email+ '''"and password ="'''+password+'''"'''
            mycursor.execute(q)
            res = mycursor.fetchall()
            if len(res)==0:
               raise Page.DoesNotExist("No Profile")

            page = Page.objects.get(email=email,password=password)
            name = page.title
            num_followers = page.numfollowers



            followed_pages = len(PageFollowsPage.objects.filter(follower_email=email))
            followed_profiles = len(PageFollowsProfile.objects.filter(follower_page_email=email))

            follower_profiles = ProfileFollowsPage.objects.filter(page_email = email).order_by('regular_profile_email')
            follower_pages = PageFollowsPage.objects.filter(followed_page_email = email).order_by('follower_email')


            followers = list(chain(follower_profiles,follower_pages))

            profile_followings = PageFollowsProfile.objects.filter(follower_page_email = email).order_by('followed_profile_email')
            page_followings = PageFollowsPage.objects.filter(follower_email = email).order_by('followed_page_email')

            followings = list(chain(profile_followings,page_followings))

            num_followed = followed_pages+followed_profiles

            albums = Album.objects.filter(page_email = page).order_by('name')


            MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
            PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))


            if not MAIN.exists():

                os.mkdir(MAIN)


            if not PROFILE_PICTURES.exists():

                profile_pics = Album.objects.create(page_email=page,name="Profile Pictures",num_photos=0)

                os.mkdir(PROFILE_PICTURES)


            CHOICES = []

            for album in albums:
                choice = (album.album_id,album.name)
                CHOICES.append(choice)




            template="indexpage.html"
            if request.method == 'POST':


                if "update_id" in request.POST:

                    update_id = request.POST.get("update_id")



                    if "num_likes" in request.POST:

                        update_likes =  request.POST.get("num_likes")

                        if "album_id" in request.POST:

                            clicked_photo = Photos.objects.filter( update_id = update_id).first()

                            print("You liked a damn photo")

                            liker = PageLikesPhotos.objects.filter(update_id = update_id, page_email = page, photo_like_id = update_id).first()

                            if liker:

                                PageLikesPhotos.objects.filter(update_id = update_id, page_email = page, photo_like_id = update_id).delete()

                                clicked_photo.num_likes = update_likes;

                                clicked_photo.save()

                            else :

                                liker = PageLikesPhotos.objects.create(update_id = update_id, page_email = page, photo_like_id = update_id)

                                clicked_photo.num_likes = update_likes;

                                clicked_photo.save()

                                likes = PageLikesPhotos.objects.filter(update = clicked_photo).order_by('page_email')

                        else:

                            clicked_update = Status.objects.filter( update_id = update_id).first()


                            liker = PageLikesStatus.objects.filter(update_id = update_id, page_email = page, status_like_id = update_id).first()

                            if liker:

                                PageLikesStatus.objects.filter(update_id = update_id, page_email = page, status_like_id = update_id).delete()

                                clicked_update.num_likes = update_likes;

                                clicked_update.save()

                            else :

                                liker = PageLikesStatus.objects.create(update_id = update_id, page_email = page, status_like_id = update_id)

                                clicked_update.num_likes = update_likes;

                                clicked_update.save()

                                likes = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')


                if "make-album" in request.POST:

                    form = AlbumForm(request.POST,request.FILES)


                    if form.is_valid():

                        name = form.cleaned_data['name']


                        if not Album.objects.filter(name = name , page_email = email):
                            album = form.save()

                            album.page_email = Page.objects.filter(email = email).first()
                            album.num_photos = 0

                            album.save()

                            album_id = album.album_id

                            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(album_id))

                            if not USER_IMAGES.exists():

                                os.mkdir(USER_IMAGES)



                if "album_id" in request.POST:
                    print("This is an album id")

                    album_id = request.POST.get("album_id")

                    clicked_album = Album.objects.filter(album_id = album_id).first()

                    album_name = clicked_album.name

                    photos = Photos.objects.filter(page_email = page, album_id = album_id).order_by('update_id')

                    form = PhotoForm(CHOICES)


                if "make-image" in request.POST:

                    form = PhotoForm(CHOICES,request.POST,request.FILES)


                    if form.is_valid():
                        print("FORM IS VALID")

                        album = Album.objects.filter(album_id = album_id).first()

                        photo = Image.open(request.FILES['photo'])

                        photof = form.save(commit=False)

                        album.num_photos += 1

                        album.save()

                        photof.page_email = page
                        photof.album = album
                        photof.date = datetime.now()
                        photof.status_id = 10
                        photof.num_likes = 0
                        photof.num_shares = 0
                        photof.city = page.city
                        photof.state = page.state
                        photof.save()

                        if album.name == "Profile Pictures":

                            if Photos.objects.filter(album = album):
                                Photos.objects.filter(album = album).delete()

                            croppedPhoto = resizer(crop(photo),170)
                            croppedPhoto35 = resizer(crop(photo),37)

                            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(page.email),str(page.email))


                            if not USER_IMAGES.exists():

                                os.mkdir(USER_IMAGES)

                            form.save()

                            LOCATION =  Path(USER_IMAGES,str(page.email)+".jpg")
                            LOCATION35 =  Path(USER_IMAGES,str(page.email)+"35.jpg")

                            croppedPhoto = croppedPhoto.convert('RGB')
                            croppedPhoto35 = croppedPhoto35.convert('RGB')

                            croppedPhoto.save(LOCATION, optimize=True, quality=85)
                            croppedPhoto35.save(LOCATION35, optimize=True, quality=70)

                        else:

                            croppedPhoto = resizer(photo,1000)
                            USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(page.email),str(album_id))


                            if not USER_IMAGES.exists():

                                os.mkdir(USER_IMAGES)

                            form.save()

                            LOCATION =  Path(USER_IMAGES,str(photof.update_id)+".jpg")

                            croppedPhoto = croppedPhoto.convert('RGB')
                            croppedPhoto.save(LOCATION, optimize=True, quality=85)



                else:

                    form = PhotoForm(CHOICES)


            else:

                form = PhotoForm(CHOICES)



            if request.is_ajax():

                album_id = request.GET.get('album_id')

                clicked_album = Album.objects.filter(album_id=album_id).first()
                photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

                template = 'album.html'

                if 'type' in request.GET:

                    if request.GET.get('type') == "followers" :

                        template = "followers.html"

                    if request.GET.get('type') == "followings" :

                        template = "followings.html"

                if "type" in request.POST:

                    if request.POST.get("type") == "page":

                        if "followed_email" in request.POST:

                            followed_email = request.POST.get("followed_email")
                            followed_page = Page.objects.filter(email = followed_email).first()

                            if not PageFollowsPage.objects.filter(followed_page_email = followed_page , follower_email = page ):
                                follow = PageFollowsPage.objects.create(followed_page_email = followed_page , follower_email = page )
                                print("followed "+followed_email)

                        if "un_followed_email" in request.POST:

                            un_followed_email= request.POST.get("un_followed_email")

                            if PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = email):
                                unfollow = PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = email).delete()
                                print("unfollowed "+un_followed_email)

                    if request.POST.get("type") == "profile":

                        if "followed_email" in request.POST:

                            followed_email = request.POST.get("followed_email")
                            followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                            if not PageFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_page_email = page):
                                follow = PageFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_page_email = page)
                                print("followed "+followed_email)

                        if "un_followed_email" in request.POST:

                            un_followed_email= request.POST.get("un_followed_email")

                            if PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = email):
                                unfollow = PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = email).delete()
                                print("unfollowed "+un_followed_email)

                if 'update_id' in request.GET:

                    update_id = request.GET.get('update_id')


                    if 'num_likes' in request.GET:

                        template = 'likes.html'


                    elif 'num_shares' in request.GET:

                        template = 'shares.html'

                    else:

                        clicked_photo = Photos.objects.filter(update_id=update_id).first()
                        template = 'album.html'


            else:

                template = 'indexpage.html'



















            pages = PageFollowsPage.objects.filter(follower_email=email)
            profiles = PageFollowsProfile.objects.filter(follower_page_email=email)
            update_id = request.GET.get('update_id')
            clicked_update = Status.objects.filter(update_id = update_id).first()
            photo_add = dict()

            shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')

            likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                    ,PageLikesStatus.objects.filter(update = clicked_update)))

            statuses = []
            names = dict()


            for each in profiles:
               stats = Status.objects.filter(regular_profile_email=each.followed_profile_email.email)
               pics = Photos.objects.filter(regular_profile_email=each.followed_profile_email.email)
               obj = RegularProfile.objects.get(email=each.followed_profile_email.email)


               for post in stats:
                  statuses.append(post)
                  names[post.update_id] = obj.firstname + " " + obj.lastname

               for pic in pics:
                   statuses.append(pic)
                   names[pic.update_id] = obj.firstname + " " + obj.lastname
                   alb_id = pic.album.album_id
                   up_id = pic.update_id
                   add = "media/"+obj.email+"/"+str(alb_id)+"/"+str(up_id)+".jpg"
                   photo_add[up_id] = add




            for each in profiles:
                shared = ProfileSharesStatus.objects.filter(regular_profile_email=each.followed_profile_email)
                p_shared = ProfileSharesPhotos.objects.filter(regular_profile_email=each.followed_profile_email)

                for sh in shared:
                    statuses.append(sh)
                for p in p_shared:
                    ph = Photos.objects.get(update_id = p.update.update_id )
                    s_mail = ""

                    if(ph.regular_profile_email is None):
                        s_mail = ph.page_email.email
                    else:
                        s_mail = ph.regular_profile_email.email


                    up_id = ph.update_id
                    alb_id = ph.album.album_id
                    add = "media/"+s_mail+"/"+str(alb_id)+"/"+str(up_id)+".jpg"
                    photo_add[up_id] = add

                    statuses.append(p)



            for each in pages:
               stats = Status.objects.filter(page_email=each.followed_page_email.email)
               photos_p  = Photos.objects.filter(page_email=each.followed_page_email.email)

               obj = Page.objects.get(email = each.followed_page_email.email)

               for post in stats:
                  statuses.append(post)
                  names[post.update_id] = obj.title

               for pic in photos_p:
                   statuses.append(pic)
                   names[pic.update_id] = obj.title
                   up_id = pic.update_id
                   alb_id = pic.album.album_id
                   add = "media/"+obj.email+"/"+str(alb_id)+"/"+str(up_id)+".jpg"





            print(statuses)
            statuses.sort(key = lambda x: x.date,reverse=True)




            profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in profile_followings])]
            page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.followed_page_email for email in page_followings])]

            profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in profile_followings])]
            page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.followed_page_email for email in page_followings])]

            profile_suggestion = set(chain(profile_following_profile,page_following_profile))
            page_suggestion = set(chain(profile_following_page,page_following_page))

            for profiles in profile_followings:
                page_suggestion.discard(profiles.follower_page_email)
                profile_suggestion.discard(profiles.followed_profile_email)
            for pages in page_followings:
                page_suggestion.discard(pages.follower_email)
                page_suggestion.discard(pages.followed_page_email)

            profile_suggestion = list(profile_suggestion)
            page_suggestion = list(page_suggestion)



            profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
            page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

            if len(profile_suggestion)>3:
                profile_suggestion = profile_suggestion[0:3]
            if len(page_suggestion)>3:
                page_suggestion = page_suggestion[0:3]

            suggestions = list(chain(profile_suggestion,page_suggestion))

            followings = list(chain(profile_followings,page_followings))


            non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                            ,Page.objects.exclude(email__in = [object.followed_page_email.email for object in page_followings])))


            followed_follower_profiles = PageFollowsProfile.objects.filter(follower_page_email = email, followed_profile_email__in = [object.regular_profile_email for object in follower_profiles] ).order_by('follower_page_email')
            followed_followers_pages = PageFollowsPage.objects.filter(follower_email = email, followed_page_email__in = [object.follower_email for object in follower_pages] ).order_by('follower_email')


            followed_followers = list(chain(followed_follower_profiles,followed_followers_pages))
            unfollowed_followers = list(chain(ProfileFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_email__in = [object.followed_profile_email for object in followed_follower_profiles])
                        ,PageFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_page_email__in = [object.follower_email for object in followed_followers_pages])))





            context = dict()
            context['email'] = email
            context['names'] = names
            context['suggestions'] = suggestions
            context['status'] = statuses
            context['name'] = name
            context['form'] = form
            context['pic_add'] = photo_add



            context['page'] = page
            context['followers'] = followers

            context['followed_followers'] = followed_followers
            context['unfollowed_followers'] = unfollowed_followers

            context['followings'] = followings
            context['non_followings'] = non_followings

            context['suggestions'] = suggestions

            context['shares'] = shares
            context['likes'] = likes
            return render(request,template,context=context)



         except  Page.DoesNotExist:

            messages.info(request,"Check Email or Password")
            print("ERROR")
            return redirect('login')


      return render(request,"index.html")




def add(request):

   if request.method == 'POST':



      caption = request.POST['caption']
      city = request.POST['mycity']
      state = request.POST['mystate']
      email = mail
      date = datetime.now()

      try:
         reg_pro = RegularProfile.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,regular_profile_email=reg_pro,caption=caption,num_likes=0,num_shares=0,city=city,state=state,date=date)
         post.save()


      except RegularProfile.DoesNotExist:
         page = Page.objects.get(email=email)
         id = Status.objects.latest().status_id+1
         post = Status(status_id=id,page_email=page,caption=caption,num_likes=0,num_shares=0,city=city,state=state,date=date)
         post.save()

      return redirect(reverse('feed'))

def addjob(request):


      email = mail

      title = request.POST.get('job_title')
      qualification = request.POST.get('qualification')
      city = request.POST.get('j_city')
      state = request.POST.get('j_state')
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
      job = Job(type=title,page_email=page,qualification=qualification,num_hours=time,num_posts=vacant,salary=cost,contact_detail=contact,city=city,state=state,postdate=date,description=desc)
      job.save()
      return redirect(reverse('feed'))



def search(request):
   email = mail
   email = request.session['email']
   profile = RegularProfile.objects.get(email=email)
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
   skills = dict()
   interests = dict()

   myresult = mycursor.fetchall()

   for each in myresult:
      emails.append(each[0])


   for each in emails:
      try:
         person = RegularProfile.objects.get(email=each)
         persons.append(person)

      except RegularProfile.DoesNotExist:

         page = Page.objects.get(email=each)
         pages.append(page)

   for person in persons:
      skill = Skills.objects.filter(email=person.email)
      skills[person.email] = skill

      interest = Interests.objects.filter(email=person.email)
      interests[person.email] = interest




   context['skills'] = skills
   context['interests'] = interests
   context['people'] = persons
   context['pages'] = pages
   context['mail'] = email
   context['profile'] = profile
   return render(request,"search.html",context=context)












def searchjobs(request):

   email = request.session['email']
   profile = RegularProfile.objects.get(email=email)

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
   applies = dict()
   myresult = mycursor.fetchall()

   for each in myresult:
      ids.append(each[0])




   for each in ids:
      job = Job.objects.get(job_id=each)
      jobs_list.append(job)
      obj = Page.objects.get(email=job.page_email.email)
      page[job.page_email] = obj.title

   job_app = []
   applies_for = AppliesFor.objects.all()
   for each in applies_for:
      if each.regular_profile_email.email == email:
         job_app.append(Job.objects.get(job_id = each.job.job_id))


   jobs = Job.objects.all()
   for each in jobs:
      if each in job_app:
         applies[each.job_id] = True

      else:
         applies[each.job_id] = False


   context = dict()
   context['jobs'] = jobs_list
   context['applies'] = applies
   context['name'] = RegularProfile.objects.get(email=email).firstname + " " + RegularProfile.objects.get(email=email).lastname
   context['page'] = page
   context['profile'] = profile


   return render(request,"searchjobs.html",context=context)





def apply(request):
   email = mail

   job = request.POST.get('job_post')
   job = int(job)
   job_instance = Job.objects.get(job_id=job)
   prof = RegularProfile.objects.get(email=email)
   inst = AppliesFor.objects.create(regular_profile_email=prof,job=job_instance)
   return redirect(reverse('jobs'))





def cancel(request):
   email = mail
   job = request.POST.get('job_post')
   job = int(job)
   job_instance = Job.objects.get(job_id=job)
   prof = RegularProfile.objects.get(email=email)
   inst = AppliesFor(regular_profile_email=prof,job=job_instance)
   inst.delete()
   return redirect(reverse('jobs'))







def jobs(request):

      email = mail
      profile = RegularProfile.objects.get(email=email)

      jobs = []
      page = dict()
      applies = dict()
      jobs = Job.objects.all()

      for each in jobs:
         obj = Page.objects.get(email=each.page_email.email)
         page[each.page_email] = obj.title



      jobs = Job.objects.all()
      appl = AppliesFor.objects.filter(regular_profile_email=mail)
      app_jobs = []
      for each in appl:
          jb = Job.objects.get(job_id = each.job.job_id)
          app_jobs.append(jb)

      for each in jobs:

         if each in app_jobs:
            applies[each.job_id] = True

         else:
            applies[each.job_id] = False



      context = dict()
      print(applies)
      context['jobs'] = jobs
      context['applies'] = applies
      context['name'] = RegularProfile.objects.get(email=email).firstname + " " + RegularProfile.objects.get(email=email).lastname
      context['page'] = page
      context['profile'] = profile

      return render(request,"jobs.html",context=context)








def signup_two(request):


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




def addimg(request):
    return

def deletejob(request):

    delid = request.POST['deleteid']
    job_id = int(delid)
    job = Job.objects.get(job_id = job_id)
    app = AppliesFor.objects.filter(job=job)
    job.delete()
    app.delete()
    return redirect(reverse('myjobs'))


def myjobs(request):
    email = mail
    pg = Page.objects.get(email=email)
    page = dict()
    applies = dict()
    jobs = Job.objects.filter(page_email=email)
    for each in jobs:
        pg = Page.objects.get(email=each.page_email.email)
        page[each.page_email] = pg.title

    for each in jobs:
        app = AppliesFor.objects.filter(job=each)
        applies[each.job_id] = app
    context = dict()
    context['jobs'] = jobs
    context['applies'] = applies
    context['page'] = page
    context['pg'] = pg


    return render(request,"myjobs.html",context=context)
















def profile(request):


    # email = mail
    email = 'abc@abc.com'

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

    # followings_ids = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
    #                 ,Page.objects.filter(email__in = [object.page_email.email for object in page_followings])))

    non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.exclude(email__in = [object.page_email.email for object in page_followings])))


    followed_follower_profiles = ProfileFollowsProfile.objects.filter(follower_email = email, followed_profile_email__in = [object.follower_email for object in follower_profiles] ).order_by('follower_email')
    followed_followers_pages = ProfileFollowsPage.objects.filter(regular_profile_email = email, page_email__in = [object.follower_page_email for object in follower_pages] ).order_by('page_email')


    followed_followers = list(chain(followed_follower_profiles,followed_followers_pages))
    unfollowed_followers = list(chain(ProfileFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_email__in = [object.followed_profile_email for object in followed_follower_profiles])
                        ,PageFollowsProfile.objects.filter(followed_profile_email = email).exclude( follower_page_email__in = [object.page_email for object in followed_followers_pages])))


    albums = Album.objects.filter(regular_profile_email = email).order_by('name')
    print(albums)


    MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
    PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))


    if not MAIN.exists():

        os.mkdir(MAIN)


    if not PROFILE_PICTURES.exists():

        profile_pics = Album.objects.create(regular_profile_email=RegularProfile.objects.filter(email = email).first(),name="Profile Pictures",num_photos=0)
        print("Does Not Exist")
        os.mkdir(PROFILE_PICTURES)






    # CHOICES = []
    # for album in albums:
    #     choice = (album.album_id,album.name)
    #     CHOICES.append(choice)
    # CHOICES = tuple(CHOICES)



    if request.method == 'POST':


        if "update_id" in request.POST:

            update_id = request.POST.get("update_id")

            if "num_likes" in request.POST:

                update_likes =  request.POST.get("num_likes")

                if "album_id" in request.POST:

                    clicked_photo = Photos.objects.filter(update_id = update_id).first()

                    print("You liked a damn photo")

                    liker = ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = profile, photo_like_id = update_id).first()

                    if liker:

                        ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = profile, photo_like_id = update_id).delete()

                        clicked_photo.num_likes = update_likes;

                        clicked_photo.save()

                    else :

                        liker = ProfileLikesPhotos.objects.create(update_id = update_id, regular_profile_email = profile, photo_like_id = update_id)

                        clicked_photo.num_likes = update_likes;

                        clicked_photo.save()

                        likes = ProfileLikesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                else:

                    clicked_update = Status.objects.filter(update_id = update_id).first()


                    liker = ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).first()

                    if liker:

                        ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, status_like_id = update_id).delete()

                        clicked_update.num_likes = update_likes;

                        clicked_update.save()

                    else :

                        liker = ProfileLikesStatus.objects.create(update_id = update_id, regular_profile_email = profile, status_like_id = update_id)

                        clicked_update.num_likes = update_likes;

                        clicked_update.save()

                        likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


            if "num_shares" in request.POST:

                update_shares =  request.POST.get("num_shares")

                if "album_id" in request.POST:

                    clicked_photo = Photos.objects.filter(update_id = update_id).first()

                    print("You shared a damn photo")

                    sharer = ProfileSharesPhotos.objects.filter(update_id = update_id, regular_profile_email = profile, share_id = update_id).first()

                    if not sharer:

                        sharer = ProfileSharesPhotos.objects.create(update_id = update_id, regular_profile_email = profile, share_id = update_id, date = datetime.now())

                        clicked_photo.num_shares = update_shares;

                        clicked_photo.save()

                        shares = ProfileSharesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                else:

                    clicked_update = Status.objects.filter(update_id = update_id).first()

                    sharer = ProfileSharesStatus.objects.filter(update_id = update_id, regular_profile_email = profile, share_id = update_id).first()

                    if not sharer:
                        date = datetime.now()

                        sharer = ProfileSharesStatus.objects.create(update_id = update_id, regular_profile_email = profile, share_id = update_id, date = datetime.now())

                        clicked_update.num_shares = update_shares;

                        clicked_update.save()

                        shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')

        if "make-album" in request.POST:

            form = AlbumForm(request.POST,request.FILES)


            if form.is_valid():

                name = form.cleaned_data['name']

                if not Album.objects.filter(name = name , regular_profile_email = email):
                    album = form.save()

                    album.regular_profile_email = RegularProfile.objects.filter(email = email).first()
                    album.num_photos = 0

                    album.save()

                    album_id = album.album_id

                    USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(album_id))

                    if not USER_IMAGES.exists():

                        os.mkdir(USER_IMAGES)

            return redirect("/profile")

        if "album_id" in request.POST:

            album_id = request.POST.get("album_id")
            clicked_album = Album.objects.filter(album_id = album_id).first()

            album_name = clicked_album.name
            photos = Photos.objects.filter( album_id = album_id).order_by('update_id')
            form = AlbumForm()


        #
        # if "make-image" in request.POST:
        #
        #     form = PhotoForm(CHOICES,request.POST,request.FILES)
        #
        #     if form.is_valid():
        #
        #         album = Album.objects.filter(album_id = album_id).first()
        #
        #         photo = Image.open(request.FILES.get('photo')) #gets image from form
        #
        #         photof = form.save(commit=False)
        #
        #         album.num_photos += 1
        #
        #         album.save()
        #
        #         photof.regular_profile_email = profile
        #
        #         photof.album = album
        #         photof.date = datetime.now()
        #
        #         photof.status_id = 10
        #         photof.num_likes = 0
        #         photof.num_shares = 0
        #         photof.city = profile.city
        #         photof.state = profile.state
        #
        #
        #         if album.name == "Profile Pictures":
        #
        #             if Photos.objects.filter(album = album):
        #                 Photos.objects.filter(album = album).delete()
        #
        #             #PROFILE PHOTO CREATION
        #
        #             croppedPhoto = resizer(crop(photo),170)
        #             croppedPhoto35 = resizer(crop(photo),37)
        #
        #             USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(profile.email),str(profile.email))
        #
        #             if not USER_IMAGES.exists():
        #
        #                 os.mkdir(USER_IMAGES)
        #
        #             form.save()
        #
        #             LOCATION =  Path(USER_IMAGES,str(profile.email)+".jpg")
        #             LOCATION35 =  Path(USER_IMAGES,str(profile.email)+"35.jpg")
        #
        #             croppedPhoto = croppedPhoto.convert('RGB')
        #             croppedPhoto35 = croppedPhoto35.convert('RGB')
        #
        #             croppedPhoto.save(LOCATION, optimize=True, quality=85)
        #             croppedPhoto35.save(LOCATION35, optimize=True, quality=70)
        #
        #
        #         else:
        #
        #             croppedPhoto = resizer(photo,1000)
        #             USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(profile.email),str(album_id))
        #
        #
        #             if not USER_IMAGES.exists():
        #
        #                 os.mkdir(USER_IMAGES)
        #
        #             form.save()
        #
        #             LOCATION =  Path(USER_IMAGES,str(photof.update_id)+".jpg")
        #
        #             croppedPhoto = croppedPhoto.convert('RGB')
        #             croppedPhoto.save(LOCATION, optimize=True, quality=85)


        else:
            form = AlbumForm()
            # form = PhotoForm(CHOICES)


    else:
        form = AlbumForm()
        # form = PhotoForm(CHOICES)


    if request.is_ajax():

        album_id = request.GET.get('album_id')

        clicked_album = Album.objects.filter(album_id=album_id).first()
        photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

        template = 'album.html'

        if 'type' in request.GET:

            if request.GET.get('type') == "followers" :

                template = "followers.html"

            if request.GET.get('type') == "followings" :

                template = "followings.html"

        if "type" in request.POST:

            if request.POST.get("type") == "page":

                if "followed_email" in request.POST:

                    followed_email = request.POST.get("followed_email")
                    followed_page = Page.objects.filter(email = followed_email).first()

                    if not ProfileFollowsPage.objects.filter(page_email = followed_page , regular_profile_email = profile ):
                        follow = ProfileFollowsPage.objects.create(page_email = followed_page , regular_profile_email = profile )
                        print("followed "+followed_email)

                if "un_followed_email" in request.POST:

                    un_followed_email= request.POST.get("un_followed_email")

                    if ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = email):
                        unfollow = ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = email).delete()
                        print("unfollowed "+un_followed_email)

            if request.POST.get("type") == "profile":

                if "followed_email" in request.POST:

                    followed_email = request.POST.get("followed_email")
                    followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                    if not ProfileFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_email = profile):
                        follow = ProfileFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_email = profile)
                        print("followed "+followed_email)

                if "un_followed_email" in request.POST:

                    un_followed_email= request.POST.get("un_followed_email")

                    if ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = email):
                        unfollow = ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = email).delete()
                        print("unfollowed "+un_followed_email)

        if 'update_id' in request.GET:

            update_id = request.GET.get('update_id')


            if 'num_likes' in request.GET:

                template = 'likes.html'


            elif 'num_shares' in request.GET:

                template = 'shares.html'

            else:

                clicked_photo = Photos.objects.filter( update_id=update_id).first()
                template = 'album.html'


    else:

        template = 'user-profile.html'


    album_id = request.GET.get('album_id')
    update_id = request.GET.get('update_id')


    clicked_album = Album.objects.filter(album_id=album_id).first()

    clicked_update = Status.objects.filter( update_id = update_id).first()
    clicked_photo = Photos.objects.filter( update_id = update_id).first()

    photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

    all_photos = Photos.objects.filter(regular_profile_email=email).order_by("?")[:9]
    update_photos = Photos.objects.filter(regular_profile_email=email)

    shares = RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in chain(ProfileSharesStatus.objects.filter(update = clicked_update),ProfileSharesPhotos.objects.filter(update = clicked_photo))])

    prof_likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                ,ProfileLikesPhotos.objects.filter(update = clicked_photo)))
    page_likes = list(chain(PageLikesStatus.objects.filter(update = clicked_update)
                ,PageLikesPhotos.objects.filter(update = clicked_photo)))

    likes = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in prof_likes])
            ,Page.objects.filter(email__in = [object.page_email.email for object in page_likes])))

    album_cover = Photos.objects.filter(regular_profile_email=email).order_by("album_id").distinct()

    shared_status = ProfileSharesStatus.objects.filter(regular_profile_email = email)
    shared_photos = ProfileSharesPhotos.objects.filter(regular_profile_email = email)

    shared_updates = list()

    for shared in shared_status:
        temp_update = Status.objects.filter(update_id = shared.update_id).first()
        shared_update = {'update_id':shared.update_id
        ,'regular_profile_email':temp_update.regular_profile_email
        ,'page_email': temp_update.page_email
        ,'caption': temp_update.caption
        ,'date':shared.date
        ,'num_shares': temp_update.num_shares
        ,'num_likes': temp_update.num_likes
        ,'city': temp_update.city
        ,'state': temp_update.state }
        shared_updates.append(shared_update)

    for shared in shared_photos:
        temp_photo = Photos.objects.filter(update_id = shared.update_id).first()
        shared_update = {'update_id':shared.update_id
        ,'album':temp_photo.album
        ,'regular_profile_email':temp_photo.regular_profile_email
        ,'page_email': temp_photo.page_email
        ,'caption': temp_photo.caption
        ,'date':shared.date
        ,'num_shares': temp_photo.num_shares
        ,'num_likes': temp_photo.num_likes
        ,'city': temp_photo.city
        ,'state': temp_photo.state }
        shared_updates.append(shared_update)

    # print([o for o in shared_updates])
    #suggestions algorithm

    profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in profile_followings])]
    page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.page_email for email in page_followings])]

    profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in profile_followings])]
    page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.page_email for email in page_followings])]

    profile_suggestion = set(chain(profile_following_profile,page_following_profile))
    page_suggestion = set(chain(profile_following_page,page_following_page))

    for profiles in profile_followings:
        profile_suggestion.discard(profiles.follower_email)
        profile_suggestion.discard(profiles.followed_profile_email)
    for pages in page_followings:
        profile_suggestion.discard(pages.regular_profile_email)
        page_suggestion.discard(pages.page_email)

    profile_suggestion = list(profile_suggestion)
    page_suggestion = list(page_suggestion)

    profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
    page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

    if len(profile_suggestion)>3:
       profile_suggestion = profile_suggestion[0:3]
    if len(page_suggestion)>3:
       page_suggestion = page_suggestion[0:3]

    suggestions = list(chain(profile_suggestion,page_suggestion))

    updates = list(chain(update,update_photos))

    updates.sort(key = lambda x: x.date,reverse=True)


    # print([l.caption for l in updates])

    context = dict()


    context['profile'] = profile

    context['status'] = update

    context['updates'] = updates

    context['shared_updates'] = shared_updates

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













def visit_profile(request , visit_email ):

    email = visit_email
    # og_email = mail
    og_email = 'abc@abc.com'

    og_profile = RegularProfile.objects.filter(email = og_email).first()

    og_profile_followings = ProfileFollowsProfile.objects.filter(follower_email = og_email).order_by('followed_profile_email')
    og_page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = og_email).order_by('page_email')

    og_followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in og_profile_followings])
                    ,Page.objects.filter(email__in = [object.page_email.email for object in og_page_followings])))

    og_non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in og_profile_followings])
                    ,Page.objects.exclude(email__in = [object.page_email.email for object in og_page_followings])))

    context = dict()

    context['og'] = og_profile
    context['type'] = "profile"
    context['og_followings'] = og_followings
    context['og_non_followings'] = og_non_followings

    if Page.objects.filter(email = email) :


        profile_pic = Photos.objects.filter(page_email = email, update_id = 1).order_by('update_id')

        page = Page.objects.filter(email = email).first()

        update = Status.objects.filter(page_email = email).order_by('update_id')

        follower_profiles = ProfileFollowsPage.objects.filter(page_email = email).order_by('regular_profile_email')
        follower_pages = PageFollowsPage.objects.filter(followed_page_email = email).order_by('follower_email')


        followers = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in follower_profiles])
                        ,Page.objects.filter(email__in = [object.follower_email.email for object in follower_pages])))


        profile_followings = PageFollowsProfile.objects.filter(follower_page_email = email).order_by('followed_profile_email')
        page_followings = PageFollowsPage.objects.filter(follower_email = email).order_by('followed_page_email')

        followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                        ,Page.objects.filter(email__in = [object.followed_page_email.email for object in page_followings])))

        albums = Album.objects.filter(page_email = page).order_by('name')

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))

        if request.method == 'POST':


            if "update_id" in request.POST:

                update_id = request.POST.get("update_id")

                if "num_likes" in request.POST:

                    update_likes =  request.POST.get("num_likes")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter(update_id = update_id).first()

                        print("You liked a damn photo")

                        liker = ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile , photo_like_id = update_id).first()

                        if liker:

                            ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile, photo_like_id = update_id).delete()

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                        else :

                            liker = ProfileLikesPhotos.objects.create(update_id = update_id, regular_profile_email = og_profile, photo_like_id = update_id)

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                            likes = ProfileLikesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                    else:

                        clicked_update = Status.objects.filter( update_id = update_id).first()


                        liker = ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id).first()

                        if liker:

                            ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id).delete()

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                        else :

                            liker = ProfileLikesStatus.objects.create(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id)

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                            likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


                if "num_shares" in request.POST:

                    update_shares =  request.POST.get("num_shares")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter( update_id = update_id).first()

                        print("You shared a damn photo")

                        sharer = ProfileSharesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile, share_id = update_id).first()

                        if not sharer:

                            sharer = ProfileSharesPhotos.objects.create(update_id = update_id, regular_profile_email = og_profile, share_id = update_id, date = datetime.now())

                            clicked_photo.num_shares = update_shares;

                            clicked_photo.save()

                            shares = ProfileSharesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                    else:

                        clicked_update = Status.objects.filter( update_id = update_id).first()

                        sharer = ProfileSharesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, share_id = update_id).first()

                        if not sharer:

                            sharer = ProfileSharesStatus.objects.create(update_id = update_id, regular_profile_email = og_profile, share_id = update_id, date = datetime.now())

                            clicked_update.num_shares = update_shares;

                            clicked_update.save()

                            shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


            elif "album_id" in request.POST:

                album_id = request.POST.get("album_id")

                clicked_album = Album.objects.filter(album_id = album_id).first()

                album_name = clicked_album.name

                photos = Photos.objects.filter( album_id = album_id).order_by('update_id')


        print("\n\n\n\n\n\n")
        print(request)
        print(request.POST)
        print(request.GET)
        print("\n\n\n\n\n\n\n")


        if request.is_ajax():

            album_id = request.GET.get('album_id')

            clicked_album = Album.objects.filter( album_id=album_id ).first()
            photos = Photos.objects.filter( album_id=album_id ).order_by("update_id")

            template = 'album.html'

            if 'update_id' in request.GET:

                update_id = request.GET.get('update_id')


                if 'num_likes' in request.GET:

                    template = 'likes.html'


                elif 'num_shares' in request.GET:

                    template = 'shares.html'

                else:

                    clicked_photo = Photos.objects.filter(update_id=update_id).first()
                    template = 'album.html'


        else:

            template = 'page-visit.html'


        album_id = request.GET.get('album_id')
        update_id = request.GET.get('update_id')


        clicked_album = Album.objects.filter(album_id=album_id).first()

        clicked_update = Status.objects.filter(update_id = update_id).first()
        clicked_photo = Photos.objects.filter(update_id = update_id).first()

        photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

        all_photos = Photos.objects.filter(page_email = email).order_by("?")[:9]

        update_photos = Photos.objects.filter(page_email = email)

        followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                        ,Page.objects.filter(email__in = [object.followed_page_email.email for object in page_followings])))

        prof_likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                    ,ProfileLikesPhotos.objects.filter(update = clicked_photo)))
        page_likes = list(chain(PageLikesStatus.objects.filter(update = clicked_update)
                    ,PageLikesPhotos.objects.filter(update = clicked_photo)))

        shares = RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in chain(ProfileSharesStatus.objects.filter(update = clicked_update)
                ,ProfileSharesPhotos.objects.filter(update = clicked_photo))])

        likes = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in prof_likes])
                ,Page.objects.filter(email__in = [object.page_email.email for object in page_likes])))

        print([l for l in likes])


        album_cover = Photos.objects.filter(page_email = email).order_by("album_id").distinct()


        updates = list(chain(update,update_photos))

        updates.sort(key = lambda x: x.date,reverse=True)

        context['page'] = page

        context['status'] = update

        context['updates'] = updates

        context['followers'] = followers

        context['followings'] = followings

        context['albums'] = albums
        context['album_id'] = album_id

        context['photos'] = photos
        context['all_photos'] = all_photos

        context['clicked_album'] = clicked_album
        context['album_cover'] = album_cover

        context['shares'] = shares
        context['likes'] = likes






    elif RegularProfile.objects.filter(email = email) :

        profile_pic = Photos.objects.filter(regular_profile_email = email, update_id = 1).order_by('update_id')
        profile = RegularProfile.objects.filter(email = email).first()

        update = Status.objects.filter(regular_profile_email = email).order_by('update_id')

        skills = Skills.objects.filter(email = email).order_by('skill')
        interests = Interests.objects.filter(email = email).order_by('interest')


        follower_profiles = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_email')
        follower_pages = PageFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_page_email')


        followers = list(chain(RegularProfile.objects.filter(email__in = [object.follower_email.email for object in follower_profiles])
                        ,Page.objects.filter(email__in = [object.follower_page_email.email for object in follower_pages])))

        print([f for f in followers])

        profile_followings = ProfileFollowsProfile.objects.filter(follower_email = email).order_by('followed_profile_email')
        page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = email).order_by('page_email')

        followings =list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.filter(email__in = [object.page_email.email for object in page_followings])))

        albums = Album.objects.filter(regular_profile_email = email).order_by('name')

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))

        if request.method == 'POST':



            if "update_id" in request.POST:

                update_id = request.POST.get("update_id")

                if "num_likes" in request.POST:

                    update_likes =  request.POST.get("num_likes")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter(update_id = update_id).first()

                        print("You liked a damn photo")

                        liker = ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile, photo_like_id = update_id).first()

                        if liker:

                            ProfileLikesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile, photo_like_id = update_id).delete()

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                        else :

                            liker = ProfileLikesPhotos.objects.create(update_id = update_id, regular_profile_email = og_profile, photo_like_id = update_id)

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                            likes = ProfileLikesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                    else:

                        clicked_update = Status.objects.filter(update_id = update_id).first()


                        liker = ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id).first()

                        if liker:

                            ProfileLikesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id).delete()

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                        else :

                            liker = ProfileLikesStatus.objects.create(update_id = update_id, regular_profile_email = og_profile, status_like_id = update_id)

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                            likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


                if "num_shares" in request.POST:

                    update_shares =  request.POST.get("num_shares")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter(update_id = update_id).first()

                        print("You shared a damn photo")

                        sharer = ProfileSharesPhotos.objects.filter(update_id = update_id, regular_profile_email = og_profile, share_id = update_id).first()

                        if not sharer:

                            sharer = ProfileSharesPhotos.objects.create(update_id = update_id, regular_profile_email = og_profile, share_id = update_id, date = datetime.now())

                            clicked_photo.num_shares = update_shares;

                            clicked_photo.save()

                            shares = ProfileSharesPhotos.objects.filter(update = clicked_photo).order_by('regular_profile_email')

                    else:

                        clicked_update = Status.objects.filter(update_id = update_id).first()

                        sharer = ProfileSharesStatus.objects.filter(update_id = update_id, regular_profile_email = og_profile, share_id = update_id).first()

                        if not sharer:

                            sharer = ProfileSharesStatus.objects.create(update_id = update_id, regular_profile_email = og_profile, share_id = update_id, date = datetime.now())

                            clicked_update.num_shares = update_shares;

                            clicked_update.save()

                            shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


            if "album_id" in request.POST:

                album_id = request.POST.get("album_id")
                clicked_album = Album.objects.filter(album_id = album_id).first()

                album_name = clicked_album.name
                print(album_name)
                photos = Photos.objects.filter( album_id = album_id).order_by('update_id')


        print("\n\n\n\n\n\n")
        print(request)
        print(request.POST)
        print(request.GET)
        print("\n\n\n\n\n\n\n")


        if request.is_ajax():

            album_id = request.GET.get('album_id')

            clicked_album = Album.objects.filter(album_id=album_id).first()
            photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

            template = 'album.html'

            if 'update_id' in request.GET:

                update_id = request.GET.get('update_id')


                if 'num_likes' in request.GET:

                    template = 'likes.html'


                elif 'num_shares' in request.GET:

                    template = 'shares.html'

                else:

                    clicked_photo = Photos.objects.filter(update_id=update_id).first()
                    template = 'album.html'


        else:

            template = 'user-profile-visit.html'


        album_id = request.GET.get('album_id')
        update_id = request.GET.get('update_id')


        clicked_album = Album.objects.filter(album_id=album_id).first()
        clicked_update = Status.objects.filter( update_id = update_id).first()
        clicked_photo = Photos.objects.filter( update_id = update_id).first()


        photos = Photos.objects.filter(regular_profile_email=email,album_id=album_id).order_by("update_id")

        all_photos = Photos.objects.filter(regular_profile_email=email).order_by("?")[:9]
        update_photos = Photos.objects.filter(regular_profile_email=email)

        shares = RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in chain(ProfileSharesStatus.objects.filter(update = clicked_update),ProfileSharesPhotos.objects.filter(update = clicked_photo))])

        prof_likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                    ,ProfileLikesPhotos.objects.filter(update = clicked_photo)))
        page_likes = list(chain(PageLikesStatus.objects.filter(update = clicked_update)
                    ,PageLikesPhotos.objects.filter(update = clicked_photo)))

        likes = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in prof_likes])
                ,Page.objects.filter(email__in = [object.page_email.email for object in page_likes])))

        print([l for l in likes])
        print([l for l in shares])

        album_cover = Photos.objects.filter(regular_profile_email=email).order_by("album_id").distinct()

        updates = list(chain(update,update_photos))

        updates.sort(key = lambda x: x.date,reverse=True)

        shared_status = ProfileSharesStatus.objects.filter(regular_profile_email = email)
        shared_photos = ProfileSharesPhotos.objects.filter(regular_profile_email = email)

        shared_updates = list()

        for shared in shared_status:
            temp_update = Status.objects.filter(update_id = shared.update_id).first()
            shared_update = {'update_id':shared.update_id
            ,'regular_profile_email':temp_update.regular_profile_email
            ,'page_email': temp_update.page_email
            ,'caption': temp_update.caption
            ,'date':shared.date
            ,'num_shares': temp_update.num_shares
            ,'num_likes': temp_update.num_likes
            ,'city': temp_update.city
            ,'state': temp_update.state }
            shared_updates.append(shared_update)

        for shared in shared_photos:
            temp_photo = Photos.objects.filter(update_id = shared.update_id).first()
            shared_update = {'update_id':shared.update_id
            ,'album':temp_photo.album
            ,'regular_profile_email':temp_photo.regular_profile_email
            ,'page_email': temp_photo.page_email
            ,'caption': temp_photo.caption
            ,'date':shared.date
            ,'num_shares': temp_photo.num_shares
            ,'num_likes': temp_photo.num_likes
            ,'city': temp_photo.city
            ,'state': temp_photo.state }
            shared_updates.append(shared_update)

        context['profile'] = profile

        context['status'] = update

        context['updates'] = updates
        context['shared_updates'] = shared_updates

        context['skills'] = skills
        context['interests'] = interests

        context['followers'] = followers

        context['followings'] = followings

        context['albums'] = albums
        context['album_id'] = album_id

        context['photos'] = photos
        context['all_photos'] = all_photos

        context['clicked_album'] = clicked_album
        context['album_cover'] = album_cover

        context['shares'] = shares
        context['likes'] = likes

    if 'type' in request.GET:

        if request.GET.get('type') == "followers" :

            template = "followers.html"

        if request.GET.get('type') == "followings" :

            template = "followings.html"

    if "type" in request.POST:

        if request.POST.get("type") == "page":

            if "followed_email" in request.POST:

                followed_email = request.POST.get("followed_email")
                followed_page = Page.objects.filter(email = followed_email).first()

                if not ProfileFollowsPage.objects.filter(page_email = followed_page , regular_profile_email = og_profile ):
                    try:
                        ProfileFollowsPage.objects.create(page_email = followed_page , regular_profile_email = og_profile )
                    except:
                        print("followed "+followed_email)

            if "un_followed_email" in request.POST:

                un_followed_email= request.POST.get("un_followed_email")

                if ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = og_profile):
                    ProfileFollowsPage.objects.filter(page_email = un_followed_email , regular_profile_email = og_profile).delete()
                    print("unfollowed "+un_followed_email)

        if request.POST.get("type") == "profile":

            if "followed_email" in request.POST:

                followed_email = request.POST.get("followed_email")
                followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                if not ProfileFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_email = og_profile):
                    try:
                        ProfileFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_email = og_profile)
                    except:
                        print("followed "+followed_email)

            if "un_followed_email" in request.POST:

                un_followed_email= request.POST.get("un_followed_email")

                if ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = og_profile):
                    ProfileFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_email = og_profile).delete()
                    print("unfollowed "+un_followed_email)



    #suggestions algorithm

    profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in og_profile_followings])]
    page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.page_email for email in og_page_followings])]

    profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in og_profile_followings])]
    page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.page_email for email in og_page_followings])]

    profile_suggestion = set(chain(profile_following_profile,page_following_profile))
    page_suggestion = set(chain(profile_following_page,page_following_page))

    for profiles in og_profile_followings:
        profile_suggestion.discard(profiles.follower_email)
        profile_suggestion.discard(profiles.followed_profile_email)
    for pages in og_page_followings:
        profile_suggestion.discard(pages.regular_profile_email)
        page_suggestion.discard(pages.page_email)

    profile_suggestion = list(profile_suggestion)
    page_suggestion = list(page_suggestion)

    profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
    page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

    if len(profile_suggestion)>3:
       profile_suggestion = profile_suggestion[0:3]
    if len(page_suggestion)>3:
       page_suggestion = page_suggestion[0:3]

    suggestions = list(chain(profile_suggestion,page_suggestion))

    updates = list(chain(update,update_photos))

    updates.sort(key = lambda x: x.date,reverse=True)

    context['suggestions'] = suggestions

    return render(request,template,context)





















def visit_page(request , visit_email):

    email = visit_email
    og_email = 'bentley@abc.com'
    # og_email = mail

    og_page = Page.objects.filter(email = og_email).first()

    og_profile_followings = PageFollowsProfile.objects.filter(follower_page_email = og_email).order_by('followed_profile_email')
    og_page_followings = PageFollowsPage.objects.filter(follower_email = og_email).order_by('followed_page_email')

    og_followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in og_profile_followings])
                    ,Page.objects.filter(email__in = [object.followed_page_email.email for object in og_page_followings])))

    og_non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in og_profile_followings])
                    ,Page.objects.exclude(email__in = [object.followed_page_email.email for object in og_page_followings])))

    context = dict()

    context['og'] = og_page
    context['type'] = "page"
    context['og_followings'] = og_followings
    context['og_non_followings'] = og_non_followings

    if Page.objects.filter(email = email) :


        profile_pic = Photos.objects.filter(page_email = email, update_id = 1).order_by('update_id')

        page = Page.objects.filter(email = email).first()

        update = Status.objects.filter(page_email = email).order_by('update_id')

        follower_profiles = ProfileFollowsPage.objects.filter(page_email = email).order_by('regular_profile_email')
        follower_pages = PageFollowsPage.objects.filter(followed_page_email = email).order_by('follower_email')


        followers = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in follower_profiles])
                        ,Page.objects.filter(email__in = [object.follower_email.email for object in follower_pages])))


        profile_followings = PageFollowsProfile.objects.filter(follower_page_email = email).order_by('followed_profile_email')
        page_followings = PageFollowsPage.objects.filter(follower_email = email).order_by('followed_page_email')

        followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                        ,Page.objects.filter(email__in = [object.followed_page_email.email for object in page_followings])))

        albums = Album.objects.filter(page_email = page).order_by('name')

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))

        if request.method == 'POST':


            if "update_id" in request.POST:

                update_id = request.POST.get("update_id")



                if "num_likes" in request.POST:

                    update_likes =  request.POST.get("num_likes")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter(update_id = update_id).first()

                        print("You liked a damn photo")

                        liker = PageLikesPhotos.objects.filter(update_id = update_id, page_email = og_page, photo_like_id = update_id).first()

                        if liker:

                            PageLikesPhotos.objects.filter(update_id = update_id, page_email = og_page, photo_like_id = update_id).delete()

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                        else :

                            liker = PageLikesPhotos.objects.create(update_id = update_id, page_email = og_page, photo_like_id = update_id)

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                            likes = PageLikesPhotos.objects.filter(update = clicked_photo).order_by('page_email')

                    else:

                        clicked_update = Status.objects.filter(update_id = update_id).first()


                        liker = PageLikesStatus.objects.filter(update_id = update_id, page_email = og_page, status_like_id = update_id).first()

                        if liker:

                            PageLikesStatus.objects.filter(update_id = update_id, page_email = og_page, status_like_id = update_id).delete()

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                        else :

                            liker = PageLikesStatus.objects.create(update_id = update_id, page_email = og_page, status_like_id = update_id)

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                            likes = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')


            elif "album_id" in request.POST:

                album_id = request.POST.get("album_id")

                clicked_album = Album.objects.filter(album_id = album_id).first()

                album_name = clicked_album.name

                photos = Photos.objects.filter(album_id = album_id).order_by('update_id')


        print("\n\n\n\n\n\n")
        print(request)
        print(request.POST)
        print(request.GET)
        print("\n\n\n\n\n\n\n")


        if request.is_ajax():

            album_id = request.GET.get('album_id')

            clicked_album = Album.objects.filter(album_id=album_id).first()
            photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

            template = 'album.html'

            if 'update_id' in request.GET:

                update_id = request.GET.get('update_id')


                if 'num_likes' in request.GET:

                    template = 'likes.html'


                elif 'num_shares' in request.GET:

                    template = 'shares.html'

                else:

                    clicked_photo = Photos.objects.filter(update_id=update_id).first()
                    template = 'album.html'


        else:

            template = 'page-visit.html'


        album_id = request.GET.get('album_id')
        update_id = request.GET.get('update_id')


        clicked_album = Album.objects.filter(album_id=album_id).first()

        clicked_update = Status.objects.filter( update_id = update_id).first()
        clicked_photo = Photos.objects.filter( update_id = update_id).first()

        photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

        all_photos = Photos.objects.filter(page_email = email).order_by("?")[:9]

        update_photos = Photos.objects.filter(page_email = email)


        shares = ProfileSharesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')


        followings = list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                        ,Page.objects.filter(email__in = [object.followed_page_email.email for object in page_followings])))

        prof_likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                    ,ProfileLikesPhotos.objects.filter(update = clicked_photo)))
        page_likes = list(chain(PageLikesStatus.objects.filter(update = clicked_update)
                    ,PageLikesPhotos.objects.filter(update = clicked_photo)))

        likes = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in prof_likes])
                ,Page.objects.filter(email__in = [object.page_email.email for object in page_likes])))

        print([l for l in likes])


        album_cover = Photos.objects.filter(page_email = email).order_by("album_id").distinct()


        updates = list(chain(update,update_photos))

        updates.sort(key = lambda x: x.date,reverse=True)

        context['page'] = page

        context['status'] = update

        context['updates'] = updates

        context['followers'] = followers

        context['followings'] = followings

        context['albums'] = albums
        context['album_id'] = album_id

        context['photos'] = photos
        context['all_photos'] = all_photos

        context['clicked_album'] = clicked_album
        context['album_cover'] = album_cover

        context['shares'] = shares
        context['likes'] = likes



    elif RegularProfile.objects.filter(email = email) :

        profile_pic = Photos.objects.filter(regular_profile_email = email, update_id = 1).order_by('update_id')
        profile = RegularProfile.objects.filter(email = email).first()

        update = Status.objects.filter(regular_profile_email = email).order_by('update_id')

        skills = Skills.objects.filter(email = email).order_by('skill')
        interests = Interests.objects.filter(email = email).order_by('interest')


        follower_profiles = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_email')
        follower_pages = PageFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_page_email')


        followers = list(chain(RegularProfile.objects.filter(email__in = [object.follower_email.email for object in follower_profiles])
                        ,Page.objects.filter(email__in = [object.follower_page_email.email for object in follower_pages])))

        print([f for f in followers])

        profile_followings = ProfileFollowsProfile.objects.filter(follower_email = email).order_by('followed_profile_email')
        page_followings = ProfileFollowsPage.objects.filter(regular_profile_email = email).order_by('page_email')

        followings =list(chain(RegularProfile.objects.filter(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.filter(email__in = [object.page_email.email for object in page_followings])))

        albums = Album.objects.filter(regular_profile_email = email).order_by('name')

        MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
        PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))

        if request.method == 'POST':



            if "update_id" in request.POST:

                update_id = request.POST.get("update_id")

                clicked_update = Status.objects.filter(update_id = update_id).first()


                if "num_likes" in request.POST:

                    update_likes =  request.POST.get("num_likes")

                    if "album_id" in request.POST:

                        clicked_photo = Photos.objects.filter(update_id = update_id).first()

                        print("You liked a damn photo")

                        liker = PageLikesPhotos.objects.filter(update_id = update_id, page_email = og_page, photo_like_id = update_id).first()

                        if liker:

                            PageLikesPhotos.objects.filter(update_id = update_id, page_email = og_page, photo_like_id = update_id).delete()

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                        else :

                            liker = PageLikesPhotos.objects.create(update_id = update_id, page_email = og_page, photo_like_id = update_id)

                            clicked_photo.num_likes = update_likes;

                            clicked_photo.save()

                            likes = PageLikesPhotos.objects.filter(update = clicked_photo).order_by('page_email')

                    else:

                        clicked_update = Status.objects.filter(update_id = update_id).first()


                        liker = PageLikesStatus.objects.filter(update_id = update_id, page_email = og_page, status_like_id = update_id).first()

                        if liker:

                            PageLikesStatus.objects.filter(update_id = update_id, page_email = og_page, status_like_id = update_id).delete()

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                        else :

                            liker = PageLikesStatus.objects.create(update_id = update_id, page_email = og_page, status_like_id = update_id)

                            clicked_update.num_likes = update_likes;

                            clicked_update.save()

                            likes = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')


            if "album_id" in request.POST:

                album_id = request.POST.get("album_id")
                clicked_album = Album.objects.filter(album_id = album_id).first()

                album_name = clicked_album.name
                print(album_name)
                photos = Photos.objects.filter(album_id = album_id).order_by('update_id')


        print("\n\n\n\n\n\n")
        print(request)
        print(request.POST)
        print(request.GET)
        print("\n\n\n\n\n\n\n")


        if request.is_ajax():

            album_id = request.GET.get('album_id')

            clicked_album = Album.objects.filter(album_id=album_id).first()
            photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

            template = 'album.html'


            if 'update_id' in request.GET:

                update_id = request.GET.get('update_id')


                if 'num_likes' in request.GET:

                    template = 'likes.html'


                elif 'num_shares' in request.GET:

                    template = 'shares.html'

                else:

                    clicked_photo = Photos.objects.filter(update_id=update_id).first()
                    template = 'album.html'


        else:

            template = 'user-profile-visit.html'


        album_id = request.GET.get('album_id')
        update_id = request.GET.get('update_id')


        clicked_album = Album.objects.filter(album_id=album_id).first()

        clicked_update = Status.objects.filter( update_id = update_id).first()
        clicked_photo = Photos.objects.filter( update_id = update_id).first()


        photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

        all_photos = Photos.objects.filter(regular_profile_email=email).order_by("?")[:9]
        update_photos = Photos.objects.filter(regular_profile_email=email)

        shares = RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in chain(ProfileSharesStatus.objects.filter(update = clicked_update),ProfileSharesPhotos.objects.filter(update = clicked_photo))])

        prof_likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
                    ,ProfileLikesPhotos.objects.filter(update = clicked_photo)))
        page_likes = list(chain(PageLikesStatus.objects.filter(update = clicked_update)
                    ,PageLikesPhotos.objects.filter(update = clicked_photo)))

        likes = list(chain(RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in prof_likes])
                ,Page.objects.filter(email__in = [object.page_email.email for object in page_likes])))

        print([l for l in likes])
        print([l for l in shares])

        album_cover = Photos.objects.filter(regular_profile_email=email).order_by("album_id").distinct()

        updates = list(chain(update,update_photos))

        updates.sort(key = lambda x: x.date,reverse=True)

        shared_status = ProfileSharesStatus.objects.filter(regular_profile_email = email)
        shared_photos = ProfileSharesPhotos.objects.filter(regular_profile_email = email)

        shared_updates = list()

        for shared in shared_status:
            temp_update = Status.objects.filter(update_id = shared.update_id).first()
            shared_update = {'update_id':shared.update_id
            ,'regular_profile_email':temp_update.regular_profile_email
            ,'page_email': temp_update.page_email
            ,'caption': temp_update.caption
            ,'date':shared.date
            ,'num_shares': temp_update.num_shares
            ,'num_likes': temp_update.num_likes
            ,'city': temp_update.city
            ,'state': temp_update.state }
            shared_updates.append(shared_update)

        for shared in shared_photos:
            temp_photo = Photos.objects.filter(update_id = shared.update_id).first()
            shared_update = {'update_id':shared.update_id
            ,'album':temp_photo.album
            ,'regular_profile_email':temp_photo.regular_profile_email
            ,'page_email': temp_photo.page_email
            ,'caption': temp_photo.caption
            ,'date':shared.date
            ,'num_shares': temp_photo.num_shares
            ,'num_likes': temp_photo.num_likes
            ,'city': temp_photo.city
            ,'state': temp_photo.state }
            shared_updates.append(shared_update)

        context['profile'] = profile

        context['status'] = update

        context['updates'] = updates
        context['shared_updates'] = shared_updates

        context['skills'] = skills
        context['interests'] = interests

        context['followers'] = followers

        context['followings'] = followings

        context['albums'] = albums
        context['album_id'] = album_id

        context['photos'] = photos
        context['all_photos'] = all_photos

        context['clicked_album'] = clicked_album
        context['album_cover'] = album_cover

        context['shares'] = shares
        context['likes'] = likes


    if 'type' in request.GET:

        if request.GET.get('type') == "followers" :

            template = "followers.html"

        if request.GET.get('type') == "followings" :

            template = "followings.html"

    if "type" in request.POST:

        if request.POST.get("type") == "page":

            if "followed_email" in request.POST:

                followed_email = request.POST.get("followed_email")
                followed_page = Page.objects.filter(email = followed_email).first()

                if not PageFollowsPage.objects.filter(followed_page_email = followed_page , follower_email = og_page ):
                    follow = PageFollowsPage.objects.create(followed_page_email = followed_page , follower_email = og_page )
                    print("followed "+followed_email)

            if "un_followed_email" in request.POST:

                un_followed_email= request.POST.get("un_followed_email")

                if PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = og_page):
                    unfollow = PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = og_page).delete()
                    print("unfollowed "+un_followed_email)

        if request.POST.get("type") == "profile":

            if "followed_email" in request.POST:

                followed_email = request.POST.get("followed_email")
                followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                if not PageFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_page_email = og_page):
                    follow = PageFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_page_email = og_page)
                    print("followed "+followed_email)

            if "un_followed_email" in request.POST:

                un_followed_email= request.POST.get("un_followed_email")

                if PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = og_page):
                    unfollow = PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = og_page).delete()
                    print("unfollowed "+un_followed_email)

    profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in og_profile_followings])]
    page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.followed_page_email for email in og_page_followings])]

    profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in og_profile_followings])]
    page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.followed_page_email for email in og_page_followings])]

    profile_suggestion = set(chain(profile_following_profile,page_following_profile))
    page_suggestion = set(chain(profile_following_page,page_following_page))

    for profiles in og_profile_followings:
        page_suggestion.discard(profiles.follower_page_email)
        profile_suggestion.discard(profiles.followed_profile_email)
    for pages in og_page_followings:
        page_suggestion.discard(pages.follower_email)
        page_suggestion.discard(pages.followed_page_email)

    profile_suggestion = list(profile_suggestion)
    page_suggestion = list(page_suggestion)

    profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
    page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

    if len(profile_suggestion)>3:
        profile_suggestion = profile_suggestion[0:3]
    if len(page_suggestion)>3:
        page_suggestion = page_suggestion[0:3]

    suggestions = list(chain(profile_suggestion,page_suggestion))

    context['suggestions'] = suggestions


    return render(request,template,context)




























def page(request):


    print("\n\n\n\n\n\n")
    print(request)
    print(request.POST)
    print(request.GET)
    print("\n\n\n\n\n\n\n")

    # email = mail
    email = 'bentley@abc.com'


    profile_pic = Photos.objects.filter(page_email = email, update_id = 1).order_by('update_id')

    # profile = RegularProfile.objects.filter(email = email).first()

    page = Page.objects.filter(email = email).first()

    update = Status.objects.filter(page_email = email).order_by('update_id')



    follower_profiles = ProfileFollowsPage.objects.filter(page_email = email).order_by('regular_profile_email')
    follower_pages = PageFollowsPage.objects.filter(followed_page_email = email).order_by('follower_email')


    followers = list(chain(follower_profiles,follower_pages))

    profile_followings = PageFollowsProfile.objects.filter(follower_page_email = email).order_by('followed_profile_email')
    page_followings = PageFollowsPage.objects.filter(follower_email = email).order_by('followed_page_email')

    followings = list(chain(profile_followings,page_followings))


    non_followings = list(chain(RegularProfile.objects.exclude(email__in = [object.followed_profile_email.email for object in profile_followings])
                    ,Page.objects.exclude(email__in = [object.followed_page_email.email for object in page_followings])))


    followed_follower_profiles = PageFollowsProfile.objects.filter(follower_page_email = email, followed_profile_email__in = [object.regular_profile_email for object in follower_profiles] ).order_by('follower_page_email')
    followed_followers_pages = PageFollowsPage.objects.filter(follower_email = email, followed_page_email__in = [object.follower_email for object in follower_pages] ).order_by('follower_email')


    followed_followers = list(chain(followed_follower_profiles,followed_followers_pages))
    unfollowed_followers = list(chain(ProfileFollowsPage.objects.filter(page_email = email).exclude( regular_profile_email__in = [object.followed_profile_email for object in followed_follower_profiles])
                        ,PageFollowsPage.objects.filter(followed_page_email = email).exclude( follower_email__in = [object.followed_page_email for object in followed_followers_pages])))



    albums = Album.objects.filter(page_email = page).order_by('name')


    MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
    PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))


    if not MAIN.exists():

        os.mkdir(MAIN)


    if not PROFILE_PICTURES.exists():

        profile_pics = Album.objects.create(page_email=page,name="Profile Pictures",num_photos=0)

        os.mkdir(PROFILE_PICTURES)


    # CHOICES = []
    #
    # for album in albums:
    #     choice = (album.album_id,album.name)
    #     CHOICES.append(choice)



    if request.method == 'POST':


        if "update_id" in request.POST:

            update_id = request.POST.get("update_id")



            if "num_likes" in request.POST:

                update_likes =  request.POST.get("num_likes")

                if "album_id" in request.POST:

                    clicked_photo = Photos.objects.filter(update_id = update_id).first()

                    print("You liked a damn photo")

                    liker = PageLikesPhotos.objects.filter(update_id = update_id, page_email = page, photo_like_id = update_id).first()

                    if liker:

                        PageLikesPhotos.objects.filter(update_id = update_id, page_email = page, photo_like_id = update_id).delete()

                        clicked_photo.num_likes = update_likes;

                        clicked_photo.save()

                    else :

                        liker = PageLikesPhotos.objects.create(update_id = update_id, page_email = page, photo_like_id = update_id)

                        clicked_photo.num_likes = update_likes;

                        clicked_photo.save()

                        likes = PageLikesPhotos.objects.filter(update = clicked_photo).order_by('page_email')

                else:

                    clicked_update = Status.objects.filter(update_id = update_id).first()


                    liker = PageLikesStatus.objects.filter(update_id = update_id, page_email = page, status_like_id = update_id).first()

                    if liker:

                        PageLikesStatus.objects.filter(update_id = update_id, page_email = page, status_like_id = update_id).delete()

                        clicked_update.num_likes = update_likes;

                        clicked_update.save()

                    else :

                        liker = PageLikesStatus.objects.create(update_id = update_id, page_email = page, status_like_id = update_id)

                        clicked_update.num_likes = update_likes;

                        clicked_update.save()

                        likes = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')


        if "make-album" in request.POST:

            form = AlbumForm(request.POST,request.FILES)


            if form.is_valid():

                name = form.cleaned_data['name']

                if not Album.objects.filter(name = name , page_email = email):
                    album = form.save()

                    album.page_email = Page.objects.filter(email = email).first()
                    album.num_photos = 0

                    album.save()

                    album_id = album.album_id

                    USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(email),str(album_id))

                    if not USER_IMAGES.exists():

                        os.mkdir(USER_IMAGES)

            return redirect("/page")


        elif "album_id" in request.POST:

            album_id = request.POST.get("album_id")

            clicked_album = Album.objects.filter(album_id = album_id).first()

            album_name = clicked_album.name

            photos = Photos.objects.filter(album_id = album_id).order_by('update_id')

            form = AlbumForm()
            # form = PhotoForm(CHOICES)

        #
        # if "make-image" in request.POST:
        #
        #     form = PhotoForm(CHOICES,request.POST,request.FILES)
        #
        #
        #     if form.is_valid():
        #
        #         album = Album.objects.filter(album_id = album_id).first()
        #
        #         photo = Image.open(request.FILES['photo'])
        #
        #         photof = form.save(commit=False)
        #
        #         album.num_photos += 1
        #
        #         album.save()
        #
        #         photof.page_email = page
        #         photof.album = album
        #         photof.date = datetime.now()
        #         photof.status_id = 10
        #         photof.num_likes = 0
        #         photof.num_shares = 0
        #         photof.city = page.city
        #         photof.state = page.state
        #
        #         if album.name == "Profile Pictures":
        #
        #             if Photos.objects.filter(album = album):
        #                 Photos.objects.filter(album = album).delete()
        #
        #             croppedPhoto = resizer(crop(photo),170)
        #             croppedPhoto35 = resizer(crop(photo),37)
        #
        #             USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(page.email),str(page.email))
        #
        #
        #             if not USER_IMAGES.exists():
        #
        #                 os.mkdir(USER_IMAGES)
        #
        #             form.save()
        #
        #             LOCATION =  Path(USER_IMAGES,str(page.email)+".jpg")
        #             LOCATION35 =  Path(USER_IMAGES,str(page.email)+"35.jpg")
        #
        #             croppedPhoto = croppedPhoto.convert('RGB')
        #             croppedPhoto35 = croppedPhoto35.convert('RGB')
        #
        #             croppedPhoto.save(LOCATION, optimize=True, quality=85)
        #             croppedPhoto35.save(LOCATION35, optimize=True, quality=70)
        #
        #         else:
        #
        #             croppedPhoto = resizer(photo,1000)
        #             USER_IMAGES =  Path(Path(__file__).resolve().parent.parent, 'media',str(page.email),str(album_id))
        #
        #
        #             if not USER_IMAGES.exists():
        #
        #                 os.mkdir(USER_IMAGES)
        #
        #             form.save()
        #
        #             LOCATION =  Path(USER_IMAGES,str(photof.update_id)+".jpg")
        #
        #             croppedPhoto = croppedPhoto.convert('RGB')
        #             croppedPhoto.save(LOCATION, optimize=True, quality=85)


        else:

            form = AlbumForm()
            # form = PhotoForm(CHOICES)


    else:

        form = AlbumForm()
        # form = PhotoForm(CHOICES)


    print("\n\n\n\n\n\n")
    print(request)
    print(request.POST)
    print(request.GET)
    print("\n\n\n\n\n\n\n")


    if request.is_ajax():

        album_id = request.GET.get('album_id')

        clicked_album = Album.objects.filter(album_id=album_id).first()
        photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

        template = 'album.html'

        if 'type' in request.GET:

            if request.GET.get('type') == "followers" :

                template = "followers.html"

            if request.GET.get('type') == "followings" :

                template = "followings.html"

        if "type" in request.POST:

            if request.POST.get("type") == "page":

                if "followed_email" in request.POST:

                    followed_email = request.POST.get("followed_email")
                    followed_page = Page.objects.filter(email = followed_email).first()

                    if not PageFollowsPage.objects.filter(followed_page_email = followed_page , follower_email = page ):
                        follow = PageFollowsPage.objects.create(followed_page_email = followed_page , follower_email = page )
                        print("followed "+followed_email)

                if "un_followed_email" in request.POST:

                    un_followed_email= request.POST.get("un_followed_email")

                    if PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = email):
                        unfollow = PageFollowsPage.objects.filter(followed_page_email = un_followed_email , follower_email = email).delete()
                        print("unfollowed "+un_followed_email)

            if request.POST.get("type") == "profile":

                if "followed_email" in request.POST:

                    followed_email = request.POST.get("followed_email")
                    followed_profile = RegularProfile.objects.filter(email = followed_email).first()

                    if not PageFollowsProfile.objects.filter(followed_profile_email = followed_profile , follower_page_email = page):
                        follow = PageFollowsProfile.objects.create(followed_profile_email = followed_profile , follower_page_email = page)
                        print("followed "+followed_email)

                if "un_followed_email" in request.POST:

                    un_followed_email= request.POST.get("un_followed_email")

                    if PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = email):
                        unfollow = PageFollowsProfile.objects.filter(followed_profile_email = un_followed_email , follower_page_email = email).delete()
                        print("unfollowed "+un_followed_email)

        if 'update_id' in request.GET:

            update_id = request.GET.get('update_id')


            if 'num_likes' in request.GET:

                template = 'likes.html'


            elif 'num_shares' in request.GET:

                template = 'shares.html'

            else:

                clicked_photo = Photos.objects.filter(update_id=update_id).first()
                template = 'album.html'


    else:

        template = 'page.html'


    album_id = request.GET.get('album_id')
    update_id = request.GET.get('update_id')


    clicked_album = Album.objects.filter(album_id=album_id).first()

    clicked_update = Status.objects.filter(update_id = update_id).first()
    clicked_photo = Photos.objects.filter(update_id = update_id).first()

    photos = Photos.objects.filter(album_id=album_id).order_by("update_id")

    all_photos = Photos.objects.filter(page_email = email).order_by("?")[:9]

    update_photos = Photos.objects.filter(page_email = email)


    shares = RegularProfile.objects.filter(email__in = [object.regular_profile_email.email for object in chain(ProfileSharesStatus.objects.filter(update = clicked_update)
            ,ProfileSharesPhotos.objects.filter(update = clicked_photo))])
    # likes = ProfileLikesStatus.objects.filter(update = clicked_update).order_by('regular_profile_email')
    # likesp = PageLikesStatus.objects.filter(update = clicked_update).order_by('page_email')

    likes = list(chain(ProfileLikesStatus.objects.filter(update = clicked_update)
            ,PageLikesStatus.objects.filter(update = clicked_update)
            ,ProfileLikesPhotos.objects.filter(update = clicked_photo)
            ,PageLikesPhotos.objects.filter(update = clicked_photo)))


    print([l for l in likes])


    album_cover = Photos.objects.filter(page_email = email).order_by("album_id").distinct()




    #suggestions algorithm


    profile_following_profile = [profile.followed_profile_email for profile in ProfileFollowsProfile.objects.filter(follower_email__in = [email.followed_profile_email for email in profile_followings])]
    page_following_page = [page.followed_page_email for page in PageFollowsPage.objects.filter(follower_email__in = [email.followed_page_email for email in page_followings])]

    profile_following_page = [page.page_email for page in ProfileFollowsPage.objects.filter(regular_profile_email__in = [email.followed_profile_email for email in profile_followings])]
    page_following_profile = [profile.followed_profile_email for profile in PageFollowsProfile.objects.filter(follower_page_email__in = [email.followed_page_email for email in page_followings])]

    profile_suggestion = set(chain(profile_following_profile,page_following_profile))
    page_suggestion = set(chain(profile_following_page,page_following_page))

    for profiles in profile_followings:
        page_suggestion.discard(profiles.follower_page_email)
        profile_suggestion.discard(profiles.followed_profile_email)
    for pages in page_followings:
        page_suggestion.discard(pages.follower_email)
        page_suggestion.discard(pages.followed_page_email)

    profile_suggestion = list(profile_suggestion)
    page_suggestion = list(page_suggestion)



    profile_suggestion.sort(key = lambda x: x.num_followers,reverse=True)
    page_suggestion.sort(key = lambda x: x.numfollowers,reverse=True)

    if len(profile_suggestion)>3:
        profile_suggestion = profile_suggestion[0:3]
    if len(page_suggestion)>3:
        page_suggestion = page_suggestion[0:3]

    suggestions = list(chain(profile_suggestion,page_suggestion))

    updates = list(chain(update,update_photos))

    updates.sort(key = lambda x: x.date,reverse=True)

    context = dict()


    context['page'] = page


    context['status'] = update

    context['updates'] = updates

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
