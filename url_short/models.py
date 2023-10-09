from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    og_url = models.URLField(max_length=300)
    url = models.CharField(max_length=50)
    user =models.ForeignKey(User, on_delete=models.CASCADE)
