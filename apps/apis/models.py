from django.db import models


class Api(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
