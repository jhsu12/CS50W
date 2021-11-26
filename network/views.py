import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Post, Follow
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
        # Get all posts
        posts = Post.objects.all()

        # Return Post in reverse chronologial order
        posts = posts.order_by("-timestamp").all()

        p = Paginator(posts, 10)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        posts = p.get_page(page_num)
        return render(request, "network/index.html", {
            'posts': posts,
            'page': page,
        })
    else:
        return HttpResponseRedirect(reverse("login"))


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


@login_required
def new_post(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get contents of post
    
    content = request.POST.get('content')

    # Create new post
    post = Post(
        user = request.user,
        content = content
    )
    post.save()

    return HttpResponseRedirect(reverse('index'))

"""
@login_required
def all_posts(request):

    # Get all posts
    posts = Post.objects.all()

    # Return Post in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    p = Paginator(posts, 2)
    page_num = request.GET.get('page', 1)
    print(page_num)
    return JsonResponse([post.serialize() for post in p.get_page(page_num)], safe=False)

""" 
            


@login_required
def profile(request, name):
    # Get the posts by name
    posts = Post.objects.filter(user__username = name)

    # Return Post in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    posts = p.get_page(page_num)

    # Get following and followers number
    following_count = Follow.objects.filter(user__username = name).count()
    followers_count = Follow.objects.filter(following__username = name).count()

    # Follow button or unfollow or non
    follow = Follow.objects.filter(user__username = request.user, following__username = name)
    button = ''

    if request.user.username == name:
        button = 'non'
        
    elif len(follow) != 0:
        button = 'Unfollow'
    else:
        button = 'Follow'
    
    return render(request, "network/profile.html", {
        "posts": posts,
        "name": name,
        "button": button,
        "following_count": following_count,
        "followers_count": followers_count,
        "page": page,
    })

@csrf_exempt
@login_required
def follow_button(request):

    if request.method == 'POST':

        # Get the data first
        data = json.loads(request.body)
        visit = data.get("visit")
        action = data.get("action")

        # User follows the profile been visited
        if action == "create":
            # Create new query in Follow model
            visit = User.objects.get(username = visit)
            follow = Follow(user = request.user, following = visit)
            follow.save()
            return JsonResponse({"message": "Follow successfully."}, status=201)

        # User unfollows the profile been visited
        else:
            follow = Follow.objects.filter(user = request.user, following__username = visit)
            follow.delete()
            return JsonResponse({"message": "Unfollow successfully."}, status=201)
    
    elif request.method == "GET":
        follows = Follow.objects.all()
        return JsonResponse([follow.serialize() for follow in follows], safe=False)

@login_required
def follower(request, profile):
    if request.method == "GET":
        followers = Follow.objects.filter(following__username = profile).count()
        return JsonResponse({"followers": followers})

@login_required
def following_posts(request):
    no_folowing_posts = False

    following_posts = []
    sort_posts = []
    # Get user's following objects
    user_following = Follow.objects.filter(user = request.user)

    for user in user_following:
        following_posts.append(user.following.posts.all())
    
    # Sort the queryset not the list (list[<queryset>])
    if len(following_posts) == 0:
        no_folowing_posts = True
    else:
        for set in following_posts:
            for post in set:
                sort_posts.append(post)
        sort_posts = sorted(sort_posts, key = lambda post: post.timestamp, reverse = True)
        #print(sort_posts)

    p = Paginator(sort_posts, 10)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    posts = p.get_page(page_num)

    return render(request, "network/following_posts.html", {
            'posts': posts,
            'page': page,
            'no_following_posts': no_folowing_posts,
        })

@login_required
@csrf_exempt
def post(request, post_id):

    post = Post.objects.get(pk = post_id)

    # Return post 
    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)
    
    # Update post
    elif request.method == "PUT":

        data = json.loads(request.body)
        action = data.get("action")

        # Save post action
        if action == "save":
            new_content = data.get("content")

            post.content = new_content
            post.save()
            return JsonResponse({
                "message": "Successfully edit."
            }, status=200)
        
        # Like or Unlike post action
        elif action == "like":
            like = data.get("liked")

            if like:
                post.liked_user.add(request.user)
                post.save()
                return JsonResponse({
                    "message": "Successfully liked post."
                }, status=200)
            else:
                post.liked_user.remove(request.user)
                post.save()
                return JsonResponse({
                    "message": "Successfully unliked post."
                }, status=200)


    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)