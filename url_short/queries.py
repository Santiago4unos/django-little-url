from .models import URL

all_data = URL.objects.all()
og_urls = URL.objects.values_list("og_url")
urls = URL.objects.values_list("url")
ids = URL.objects.values_list("id")

urls_with_id = {}

for i in range(len(urls)):
    urls_with_id.update({list(urls)[i]: list(ids)[i]})

allowed_urls = []

for i, url_and_id in enumerate(urls_with_id.items()):
    if all_data[i].url == url_and_id[0][0] and all_data[i].id == url_and_id[1][0]:
        allowed_urls.append(url_and_id[0][0])