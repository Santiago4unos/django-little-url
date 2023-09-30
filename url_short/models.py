from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



class URL(models.Model):
    og_url = models.URLField(max_length=300)
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=50)

    def validate_url(self, url):
        url_validator = URLValidator(schemes=['http', 'https'])
        try:
            url_validator(url)
        except ValidationError:
            raise ValidationError("La URL no es válida")