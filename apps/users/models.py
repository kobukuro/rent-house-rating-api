from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from apps.roles.models import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password, role_name, **extra_fields):
        email = self.normalize_email(email)
        role_id = Role.objects.get(name=role_name).id
        user = self.model(email=email, role_id=role_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, role_name='admin', **extra_fields):
        return self.create_user(email, password, role_name, **extra_fields)


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
