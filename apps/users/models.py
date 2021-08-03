from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# 需要預設user的欄位就使用AbstractUser，不要就使用AbstractBaseUser
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'  # unique identifier field
