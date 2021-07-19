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
    path('signup2',views.signup2,name = 'signup2'),
    path('myjobs',views.myjobs,name = 'myjobs'),
    path('index',views.index,name = 'index'),
    path('profile',views.profile,name = 'profile'),
    path("create",views.create,name="create"),
    path("editprofile",views.editprofile,name="editprofile"),
    path("changepassword",views.changepassword,name="changepassword"),
    path("changepassword2",views.changepassword2,name="changepassword2"),
    path("changedp",views.changedp,name="changedp"),
    path("changedp2",views.changedp2,name="changedp2"),
    path("createpage",views.createpage,name="createpage"),
    path("editpage",views.editpage,name="editpage"),
    path('profile/<str:visit_email>',views.visit_profile,name = 'visit_profile'),
    path('page/<str:visit_email>',views.visit_page,name = 'visit_page'),
    path('page',views.page,name = 'page'),
    path('addjob',views.addjob,name = 'addjob'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
