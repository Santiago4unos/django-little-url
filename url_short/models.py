from django.db import models
from django.contrib.auth.models import User

class URL(models.Model):
    og_url = models.URLField(max_length=300)
    url = models.CharField(max_length=50)
    user =models.ForeignKey(User, on_delete=models.CASCADE)

class Stats(models.Model):
    url = models.OneToOneField(URL, on_delete=models.CASCADE)
    clicks = models.IntegerField()

class Referrers(models.Model):  
    stats = models.OneToOneField(Stats, on_delete=models.CASCADE)

class KeyVal(models.Model):
    container = models.ForeignKey(Referrers, db_index=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=240, db_index=True)
    value = models.IntegerField(db_index=True)

