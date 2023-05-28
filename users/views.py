from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from .models import User
from django.db import IntegrityError

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    else:
        return render(request, "users/index.html")

def login_view(request):
    if request.method=="POST":
        username= request.POST["username"]
        password= request.POST["password"]
        
        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username AND/OR password."
            })
    else:
        return render(request, "users/login.html")    


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method== "POST":
        username= request.POST["username"]
        email= request.POST["email"]
        password= request.POST["password"]
        confirmation= request.POST["confirmation"]

        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "passwords must match!"
            })
        try:
            user=User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html")