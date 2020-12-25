from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from operator import itemgetter
import mysql.connector
# Create your views here.

def welcome(request):
   return render(request,"welcome.html")


def login(request):

   mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database = "konnect_me"
   )

   mycursor = mydb.cursor()
   mycursor.execute("select email from regular_profile")

   e = []

   for each in mycursor:
      e.append(each)




   
   mycursor.execute("select password from regular_profile")

   p= []

   for each in mycursor:
      p.append(each)
   
   e = list(map(itemgetter(0),e))
   p = list(map(itemgetter(0),p))


   if request.method == "POST":
      email = request.POST["email"]
      password = request.POST["password"]

      i = 0
      while i<len(e):
         if e[i] == email and p[i] == password:
            return render(request,"index.html",{"email":email})
         i += 1


      else:
         messages.info(request,"Check Email or Password")
         return redirect('login')
      

   return render(request,"sign-in.html")

def signup(request):
   return render(request,"sign-in.html")