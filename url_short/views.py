from django.http import Http404
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import URL, Stats, Referrers, KeyVal
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from urllib.parse import urlparse

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
                url_obj = URL.objects.create(og_url=og_url, url=url, user=user)
                url_id = url_obj.id
                stats_obj = Stats.objects.create(clicks=0, url_id=url_id)
                stats_id = stats_obj.id
                referrer_obj = Referrers.objects.create(stats_id=stats_id)
                referrer_obj.save()
                url_obj.save()
                stats_obj.save()
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

        url_obj = URL.objects.get(url=url)
        stats_obj = Stats.objects.get(url_id=url_obj.id)
        stats_id = stats_obj.id
        stats_obj.clicks += 1
        stats_obj.save()

        referrer_dict = Referrers.objects.get(stats_id=stats_id)
        referrer_obj_id = referrer_dict.id

        # headers = request.headers
        # headers_keys_list = [header for header in headers]
        # headers_values_list = [header for header in headers.values()]
        # headers = zip(headers_keys_list, headers_values_list)

        if "Referer" in request.headers:
            referrer_policy = request
            referrer = request.headers["Referer"]
            referrer = urlparse(referrer).netloc if urlparse(referrer).netloc != "youtu.be" else "Youtube"
            try:
                key_val_obj = get_object_or_404(KeyVal, key=referrer)
                key_val_obj.value += 1
                key_val_obj.save()
            except Http404:
                key_val_obj = KeyVal.objects.create(container=referrer_obj_id, key=referrer, value=1)
                key_val_obj.save()
        return redirect(url_obj.og_url)
    except URL.DoesNotExist:
        raise Http404
    
def register(request):
    user_is_logged_in = request.user.is_authenticated
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect(reverse("login"))
    return render(request, "register.html", {"user_is_logged_in": user_is_logged_in})


def login_page(request):
    user_is_logged_in = request.user.is_authenticated
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("home"))
    return render(request, "login.html", {"user_is_logged_in": user_is_logged_in})

def logout_page(request):
    logout(request)
    return redirect(reverse("home"))
    
@login_required
def user_urls(request):
    if request.method == "POST":
        new_name = request.POST["new-name"]
        new_name = new_name.replace(" ", "-")
        new_url = request.POST["new-url"]
        url_id = request.POST["url_id"]
        url_obj = URL.objects.get(id=url_id)
        url_obj.url = new_name if new_name != "" else url_obj.url
        url_obj.og_url = new_url if new_url != "" else url_obj.og_url

        url_obj.save()
        try:
            delete = request.POST["delete"]
            if delete != "":
                url_obj = URL.objects.get(id=url_id)
                url_obj.delete()
                
        except KeyError:
            pass
            

    user_id = request.user.id
    owned_urls = URL.objects.filter(user_id=user_id)

    url_list = [url.url for url in owned_urls]
    og_url_list = [url.og_url for url in owned_urls]

    img_og_urls = []

    for og_url in og_url_list:
        path_netloc = urlparse(og_url).netloc
        if "youtu.be" in path_netloc:
            path_netloc = "youtube.com"
        url_img = f"https://www.google.com/s2/favicons?domain={path_netloc}"
        
        img_og_urls.append(url_img)
    
    id_list = [url.id for url in owned_urls]

    og_url_and_id_list = zip(og_url_list, id_list)
    urls_with_img = zip(url_list, img_og_urls)
    owned_urls = zip(urls_with_img, og_url_and_id_list)

    return render(request, "user_urls.html", {"owned_urls": owned_urls})    

@login_required
def my_url(request, pk):
    url_obj = URL.objects.get(id=pk)
    stats_obj = Stats.objects.get(url_id=pk)
    stats_id = stats_obj.id
    clicks = stats_obj.clicks
    referrer_dict = Referrers.objects.get(stats_id=stats_id)
    values_and_keys = KeyVal.objects.filter(container=stats_id)
    
    keys = [obj.key for obj in values_and_keys]
    values = [obj.value for obj in values_and_keys]
    referrer_dict = zip(keys, values)

    user_id = request.user.id
    if user_id == url_obj.user_id:
        return render(request, "my_url.html", {"url_obj": url_obj, "clicks": clicks , "referrer_dict": referrer_dict})
    raise Http404