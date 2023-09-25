from django.db import models

class URLManager(models.Manager):
    def create_url(self, og_url, url):
        url = self.create(og_url=og_url, url=url)
        return url

class URL(models.Model):
    og_url = models.URLField(max_length=300)
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=50)

    objects = URLManager()