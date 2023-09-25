from django.urls import path
from .models import URL
from . import views

all_data = URL.objects.all()
urls = URL.objects.values_list("url")
ids = URL.objects.values_list("id")

urls_with_id = {}

for i in range(len(urls)):
    urls_with_id.update({list(urls)[i]: list(ids)[i]})


# for i, url_and_id in enumerate(urls_with_id.items()):
#     print(i)
#     print(url_and_id[0])
#     print(url_and_id[1])

urlpatterns = []

for i, url_and_id in enumerate(urls_with_id.items()):
    if all_data[i].url == url_and_id[0][0] and all_data[i].id == url_and_id[1][0]:
        print(url_and_id[0][0])
        urlpatterns.append(path(url_and_id[0][0], views.url_redirect, name="url_redirect"))


# urlpatterns = [url_and_id[0][0] for i, url_and_id in enumerate(urls_with_id.items()) if all_data[i].url == url_and_id[0][0] and all_data[i].id == url_and_id[1][0]]