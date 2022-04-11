from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Role(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField(null=True)


from apps.system.manager import UserManager


# 需要預設user的欄位就使用AbstractUser，不要就使用AbstractBaseUser
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)
    role = models.ForeignKey(Role, db_constraint=True, related_name='system.User.role+', on_delete=models.CASCADE,
                             null=True)
    is_superuser = models.BooleanField(null=False, default=False)
    USERNAME_FIELD = 'email'  # unique identifier field
    REQUIRED_FIELDS = ['username']  # createsuperuser時會要求填這些欄位
    objects = UserManager()


class Api(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)


class ApiPrivileges(models.Model):
    api = models.ForeignKey(Api, related_name='api', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='system.ApiPrivileges.role+', on_delete=models.CASCADE)
    privilege = models.IntegerField(null=False)
