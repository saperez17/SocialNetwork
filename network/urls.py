from django.urls import path
from django.contrib import admin
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("following", views.following_view, name="following"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("api/v1/tweets/", views.tweets, name="tweets"),
    path("api/v1/like/", views.like, name="like"),
    path("api/v1/follow/", views.follow, name="follow"),
    path('profile_page/<str:username>/', views.profile_view, name="profile_page"),
    # path('profile_page/?P<str:username>/', views.profile_view, name="profile_page"),
    
]
