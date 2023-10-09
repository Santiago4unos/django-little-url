from django.http import Http404
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from .queries import allowed_urls
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    if request.method == "POST":
        og_url = request.POST["og_url"]
        url = request.POST["url"]
        url = url.replace(" ", "-")
        # user = authenticate(request, username=username, email=email, password=password)
        user_is_logged_in = request.user.is_authenticated
        user = request.user
        val = URLValidator()
        try:
            get_object_or_404(URL, url=url)
            error = "Ese nombre ya fue usado"
            return render(request, "home_error.html", {"error": error})
        except Http404:
            try:
                val(og_url)
                URL.objects.create(og_url=og_url, url=url)
            except ValidationError:
                error = "La URL no es válida"
                return render(request, "home_error.html", {"error": error})
        return render(request, "home.html", {"user_is_logged_in": user_is_logged_in, "user": user})
    elif request.user.is_authenticated:
        user = request.user
        user_is_logged_in = True
        return render(request, "home.html", {"user_is_logged_in": user_is_logged_in, "user": user})
    return render(request, "home.html")

def url_redirect(request):
    try:
        url = request.path
        url = url.replace("/", "")
        urls = URL.objects.values_list("url")
        ids = URL.objects.values_list("id")


        urls_with_id = {}

        for i in range(len(urls)):
            urls_with_id.update({list(urls)[i]: list(ids)[i]})

        og_url = URL.objects.get(url=url).og_url
        return redirect(og_url)
    except URL.DoesNotExist:
        raise Http404
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect(reverse("login"))
    return render(request, "register.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("home"))
    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return render(request, "home.html")
    
def user_urls(request):
    return render(request, "user_urls.html")
