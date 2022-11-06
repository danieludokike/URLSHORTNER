from email import message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse


import random
import string

from .models import Urls


def home_view(request):
    """Renders the home page on request"""
    if request.user.is_authenticated:
        urls = Urls.objects.filter(user=request.user).order_by("-id")
        return render(request, "myapp/index.html", {"urls": urls})
    messages.error(request, "Login required to access saved urls")
    return redirect("myapp:user_login")


def register_view(request):
    """HANDLES THE USER REGISTRATION"""
    if request.method == "POST":
        # GETTING USER INPUTS
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)
        
        if password != password2:
            messages.error(request, "Passwords must match!")
            return redirect("myapp:register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("myapp:register")
        # CHECKING TO SEE ALL FIELDS ARE FILLED
        if password is not None and username is not None:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Something went wrong. Consider login in directly")
                return redirect("myapp:user_login")
            login(request, user)
            return redirect("/")
        
        messages.error(request, "All field are required! And the asswords must match")
        return redirect("myapp:register")
            
    return render(request, "myapp/register.html")


def user_login(request):
    """HANDLES THE USER LOGIN"""
    
    if request.method == "POST":
        # GETTING USER INPUTS
        username=request.POST.get("username", None)
        password=request.POST.get("password", None)
        
        # AUTHENTICATING USER
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/")
        messages.error(request, "Invalid username or password")
        return redirect("myapp:user_login")
    return render(request, "myapp/login.html")


def user_logout(request):
    """LOGS OUT A USER"""
    logout(request)
    messages.info(request, "Session terminated. You have to login again*")
    return redirect("myapp:user_login")


def add_url_view(request):
    """ADDS THE USER IN THE URLS TABLE"""
    url = request.POST.get("url", None)
    if url is None:
        messages.error(request, "Please enter a url!")
        return redirect("/")
    rand_name = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)))
    shortened_url = f"{request.get_host()}/{rand_name}"
    
    # Checking if the shortened url or the url already exists
    if Urls.objects.filter(shortened_url=shortened_url).exists():
        messages.error(request, "URL/Shortened URL already exits. Try again!")
        return redirect("/")
    # Getting the current user
    try:
        user = User.objects.get(username=request.user)
    except:
        messages.error(request, "Login required to complete tasks!")
        return redirect("myapp:user_login")
    url_inst = Urls.objects.create(user=user, url=url, shortened_url=shortened_url)
    url_inst.save()
    messages.info(request, "URL added successfully *")
    return redirect("/")


def delete_url_view(request, id):
    """DELETES THE PARTICULARE ULR ON REQUEST"""
    try:
        url = Urls.objects.get(id=id)
    except:
        messages.error(request, "URL NOT FOUND")
        return redirect("/")
    # DELETING THE URL IF FOUND
    url.delete()
    messages.error(request, "Item Deleted Successfully")
    return redirect("/")


def get_url(request, slug):
    """GET AND REDIRECT TO THE URL OF THE SHORTENED URL"""
    shortened_url = f"{request.get_host()}/{slug}"
    # CHECKING IF THE SHORTENED URL IS IN THE Urls MODEL
    if Urls.objects.filter(shortened_url=shortened_url).exists():
        url_inst = Urls.objects.get(shortened_url=shortened_url)
        url = url_inst.url 
        
        return redirect(url)
    messages.error(request, "URL not found. Login to see urls")
    return redirect("myapp:user_login")


def text_to_speech_view(request):
    """CONVERTS TEXT TO SPEECH"""
    return render(request, "myapp/text-speech.html")
