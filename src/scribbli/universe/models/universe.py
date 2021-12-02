from django.db import models


class Universe(models.Model):
    slug = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

