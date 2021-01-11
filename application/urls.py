from django.contrib import admin
from django.urls import path, include
from application import views


urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('login',views.login,name = 'login'),
    path('feed',views.feed,name = 'feed'),
    path('add',views.add,name = 'add'),
    path('jobs',views.jobs,name = 'jobs'),
    path("searchjobs",views.searchjobs,name='searchjobs'),
    path("search",views.search,name="search")
    
]
