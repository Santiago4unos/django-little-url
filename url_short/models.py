from django.db import models

class URL(models.Model):
    og_url = models.URLField(max_length=300)
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=50)