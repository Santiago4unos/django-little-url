from django.contrib import admin
from .models import URL, Stats, Referrers, KeyVal

# Register your models here.
admin.site.register([URL, Stats, Referrers, KeyVal])