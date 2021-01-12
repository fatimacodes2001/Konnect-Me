from django.contrib import admin
from django.urls import path, include
from application import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('login',views.login,name = 'login'),
    path('feed',views.feed,name = 'feed'),
    path('add',views.add,name = 'add'),
    path('jobs',views.jobs,name = 'jobs'),
    path("searchjobs",views.searchjobs,name='searchjobs'),
    path("search",views.search,name="search"),
    path('signup_two',views.signup_two,name = 'signup_two'),
    path('index',views.index,name = 'index'),
    path('profile',views.profile,name = 'profile'),
    path('addjob',views.addjob,name = 'addjob'),


]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
