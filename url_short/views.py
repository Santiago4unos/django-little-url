from django.http import Http404
from django.urls import path
from django.shortcuts import render, HttpResponse, redirect
from .models import URL
from .queries import og_urls, allowed_urls

urlpatterns = []

def home(request):

    for url in allowed_urls:
        urlpatterns.append(path(f"{url}/", url_redirect, name="url_redirect"))
    if request.method == "POST":
        url = request.POST["url"]
        og_url = request.POST["url_name"]
        url_obj = URL.objects.create_url(url, og_url)
        return render(request, "home.html")
    return render(request, "home.html")

def url_redirect(request):
    try:
        path = request.path.replace("/urls/", "")
        path = path.replace("/", "")
        url_index = allowed_urls.index(path)
        return redirect(og_urls[url_index][0])
    except IndexError:
        raise Http404
