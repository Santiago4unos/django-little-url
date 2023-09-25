from django.http import Http404
from django.shortcuts import render, HttpResponse, redirect
from .queries import all_data, urls, ids, urls_with_id, og_urls, allowed_urls

def home(request):
    return render(request, "home.html")
    # return redirect("https://platzi.com/new-home/")

def url_redirect(request):
    try:
        url_index = allowed_urls.index(request.path.replace("/urls/", ""))
        return redirect(og_urls[url_index][0])
    except IndexError:
        raise Http404
    

    # return redirect()

    # return render(request, "urls.html", {
    #    "urls": urls,
    #     "url_names": url_names
    #     })
