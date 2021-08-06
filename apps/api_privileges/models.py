from django.db import models
from apps.apis.models import Api
from apps.roles.models import Role


class ApiPrivileges(models.Model):
    api = models.ForeignKey(Api, related_name='apis', on_delete=models.CASCADE)

    privilege = models.IntegerField(null=False)
