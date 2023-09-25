from django.urls import path
from . import views
from .queries import allowed_urls

urlpatterns = []

for url in allowed_urls:
    urlpatterns.append(path(f"{url}/", views.url_redirect, name="url_redirect"))

