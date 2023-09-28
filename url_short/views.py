from django.http import Http404
from django.core.exceptions import ValidationError
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from .queries import allowed_urls


def home(request):
    if request.method == "POST":
        og_url = request.POST["og_url"]
        url = request.POST["url"]
        url = url.replace(" ", "-")
        try:
            get_object_or_404(URL, url=url)
            error = "That name was already used"
            return render(request, "home_error.html", {"error": error})
        except Http404:
            try:
                URL.objects.create(og_url=og_url, url=url)
            except Exception:
                error = "The URL is not valid"
                return render(request, "home_error.html", {"error": error})
        return render(request, "home.html")
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

urlpatterns = []

for url in allowed_urls:
    urlpatterns.append(path(f"{url}/", url_redirect, name="url_redirect"))