from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
import string
import random

from .models import User, URL

# Create your views here.
def index(request):
    if request.method == "POST":
        original = request.POST.get('original')

        url = URL.objects.filter(original=original).first()
        if url:
            short = request.build_absolute_uri('/')+url.short
            return render(request, 'shortly/index.html', {
                'short':short
            })
        else:
            short = shortify()
            short_url=request.build_absolute_uri('/')+short
            url = URL(original=original, short=short)
            url.save()
            return render(request, 'shortly/index.html', {
                'short':short_url
            })
    return render(request, 'shortly/index.html')

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
            return render(request, "shortly/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "shortly/login.html")


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
            return render(request, "shortly/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shortly/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shortly/register.html")

def shortify():
    char = string.ascii_letters+string.digits
    short=''.join(random.choice(char) for i in range (5))
    while URL.objects.filter(short=short).exists():
        short=''.join(random.choice(char) for i in range (5))
    return short

def Redirection(request, short):
    url = URL.objects.get(short=short)

    if url:
        return redirect(url.original)
    else:
        return HttpResponse("URL not found", status=404)