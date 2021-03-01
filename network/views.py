from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
#Django settings
from django.conf import settings



from .models import User, Tweet, Like, Follower
from .serializers import TweetSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

import json


from datetime import datetime

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def index(request):
    tweets = Tweet.objects.all()
    paginator = Paginator(tweets, 10)
    # print(paginator.page_range)
    return render(request, "network/index.html",{
        "pages_range": paginator.page_range
    })

def following_view(request):
    #Filter users following this user and returned them back with the view as part of the context
    user = User.objects.get(username=request.user)
    following_list = User.objects.all().filter(pk__in=user.following.all().values('following'))
    pk = []
    for i in following_list.values('pk'):
        pk.append(int(i['pk']))
    
    tweets = Tweet.objects.all().filter(user__in=pk)
    

    # .order_by('-datetime')
    print(tweets)
    related_users = user.following.all()
    tweets_list = []
    return render(request, "network/following_page.html", {
        "data": tweets
    })

def profile_view(request, username):
    print(username)
    user = User.objects.get(username=username)
    tweets = user.tweets.all()
    tweet_serializer = TweetSerializer(tweets, many=True)
    user_serializer = UserSerializer(user)
    print(request.user.is_authenticated)
    # login(request, user)
    check = any(item in User.objects.get(username=request.user).following.all() for item in user.follower.all())
    if (check is True):
        follow_status = True
    else:
        follow_status = False
    # print(follow_status)
    return render(request, "network/user_profile.html", {
        "my_user":user_serializer.data,
        "tweets": tweet_serializer.data,
        "my_user_str": str(request.user),
        "follow": follow_status
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def queryTweets():
    pass



# @csrf_exempt
@api_view(['GET','POST'])
def tweets(request, *args, **kwargs):
    try: 
         user = User.objects.get(username=request.user)
    except:
        return Response({"message": "User not found"})
    if request.method == 'POST':
        if('pk' in request.data.keys()):
            updated_tweet = Tweet.objects.get(pk=request.data['pk'])
            updated_tweet.content = request.data['data']
            updated_tweet.save()
        new_tweet = Tweet.objects.create(user=User.objects.get(username=request.user), content=request.data['data'])
        serializer = TweetSerializer(new_tweet)
        new_tweet.save()
        return JsonResponse({"message":"Tweet added", "data":serializer.data}, status=200)
    elif request.method == 'GET':
        tweets = Tweet.objects.all()
        paginator = Paginator(tweets, 10)
        if('page' in request.GET.keys()):
            page_number = request.GET['page']
            page_obj = paginator.get_page(page_number)
            serializer = TweetSerializer(page_obj, many=True) 
        else:
            serializer = TweetSerializer(tweets, many=True)
        liked_posts = user.likes_users.all() #Like queryset
        pk_liked_posts = []
        for i in liked_posts:
            pk_liked_posts.append(i.tweet.pk)
        return Response([serializer.data, pk_liked_posts, paginator.num_pages])
    # return JsonResponse({
    #             "success": f"User with {request.user} email does not exist."
    #         }, status=200)

@api_view(['GET','POST', 'DELETE'])
def like(request, *args, **kwargs):
    try: 
        tweet = Tweet.objects.get(pk=request.data['pk'])
    except:
        return Response({"message": "Tweet not found"})
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        like_obj = Like.objects.create(user=user, tweet=tweet)
        # tweet.likes += 1
        # print(num)
        tweet.save()
        return JsonResponse({"message":"Like Added"}, status=200)
    elif request.method=='GET':
        return JsonResponse({"message":"Fetch successful",
                             "pk": request.data['pk'],
                             "likes": tweet.likes}, status=200)
    elif request.method == 'DELETE':
        # tweet = Tweet.objects.get(pk=request.data['pk'])
        user = User.objects.get(username=request.user)
        # print(user.likes_users.all()[0].tweet.pk)
        # for i in user.likes_users.all():
        #     if()
        user.likes_users.filter(id_liked_tweet=request.data['pk']).delete()
        Tweet.objects.get(pk=request.data['pk']).save()
        return JsonResponse({"message":"Fetch successful",
                             }, status=200)

@api_view(['GET', 'POST', 'DELETE'])
def follow(request, *args, **kwargs):
    if request.method == "POST":
        this_user = User.objects.get(username=request.user)
        followed_user = User.objects.get(username=request.data['follower_username'])
        follower_obj = Follower.objects.create(follower=this_user, following=followed_user)
        follower_obj.save()
        this_user.save()
        # print(follower_obj)
        return JsonResponse({"message": "User followed successfully"}, status=200)
    elif request.method == 'DELETE':
        this_user = User.objects.get(username=request.user)
        followed_user = User.objects.get(username=request.data['follower_username'])
        this_user.following.filter(following=followed_user).delete()
        this_user.save()
        # print(follower_obj)
        return JsonResponse({"message": "User followed successfully"}, status=200)
