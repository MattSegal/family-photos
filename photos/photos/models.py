from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()

