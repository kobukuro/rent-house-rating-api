from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField(null=True)
    is_superuser = models.BooleanField(default=False)
