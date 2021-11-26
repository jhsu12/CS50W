import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User, Player


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        #return render(request, "recorder/index.html")
        return render(request, "recorder/record.html")
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
            return render(request, "recorder/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recorder/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):


    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recorder/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recorder/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recorder/register.html")


def create_players(request):

    #Get the current players and sort by numbers
    players = Player.objects.filter(team=request.user).order_by('number')
    return render(request, "recorder/create_players.html", {
        "players": players,
    })


@login_required
@csrf_exempt
# create players query
def create(request):

    players = Player.objects.filter(team=request.user)
    print(players)
    # Return Player contents
    if request.method == "GET":
        return JsonResponse([player.serialize() for player in players], safe=False)

    # Create New Player
    elif request.method == "PUT":
        data = json.loads(request.body)
        
        # Get data
        team = request.user
        name = data.get("name")
        number = data.get("number")
        image = data.get("image")
        position = data.get("position")

        try:
            #new_player = Player(team=team, name=name, number=number, image=image, position=position)
            #new_player.save()
            return JsonResponse({
                "successful": f"Successfully created Player {name}, #{number}!",
                "name": name,
                "number": number,
                
            }, status=200)
        except:
            return JsonResponse({
                "error": "Make sure player's name and number are unique!"
            }, status=400)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def create_recording(request):
    #Get the current players and sort by numbers
    players = Player.objects.filter(team=request.user).order_by('number')
    return render(request, "recorder/create_recording.html", {
        "players": players,
    })