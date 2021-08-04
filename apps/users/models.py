from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.roles.models import Role
from apps.users.manager import UserManager


# 需要預設user的欄位就使用AbstractUser，不要就使用AbstractBaseUser
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)
    role = models.ForeignKey(Role, related_name='roles', on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'  # unique identifier field
    REQUIRED_FIELDS = ['username']  # createsuperuser時會要求填這些欄位
    objects = UserManager()
