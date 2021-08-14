from django.contrib.auth.models import BaseUserManager
from apps.system.models import Role
from rent_house_rating_api.enumerations import RoleType


class UserManager(BaseUserManager):
    def create_user(self, email, password, role_name, **extra_fields):
        email = self.normalize_email(email)
        if role_name == '':
            user = self.model(email=email, is_superuser=True, **extra_fields)
        else:
            role_id = Role.objects.get(name=role_name).id
            user = self.model(email=email, role_id=role_id, is_superuser=False, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, role_name='', **extra_fields):
        return self.create_user(email, password, role_name, **extra_fields)
